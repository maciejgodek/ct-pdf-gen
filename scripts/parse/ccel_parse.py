from lxml import html
import requests
from parse.latex_wrappings import *


def parse_ccel_footnote(footnote):
    text = ""
    textspan = footnote.find("span")
    length = 0
    if textspan is not None:
        if textspan.text is not None:
            text += textspan.text.lstrip().split('[', 1)[-1]
            length += len(text)
        for child in textspan:
            if child.tag == "i" and child.text is not None:
                text += latex_italic(child.text)
                length += len("".join(child.text.split()))
            elif child.tag == "span" and "Greek" in child.classes and child.text is not None:
                text += latex_greek(child.text)
                length += len("".join(child.text.split()))
            elif child.text is not None:
                text += child.text
                length += len("".join(child.text.split()))
            if child.tail is not None:
                text += child.tail
                length += len("".join(child.tail.split()))

        text = text.rstrip().translate({ord(c): None for c in "[]"}) 
        if text and length <= 60:
            return latex_margin(text)
        elif text and length > 60:
            return latex_footnote(text)
        else:
            return ""
    else:
        return ""



def parse_ccel_paragraph(p):
    text = ""
    if p.text is not None:
        text += p.text
    for child in p:
        if child.tag == "span":
            if "mnote" in child.classes:
                text += parse_ccel_footnote(child)
            elif "Greek" in child.classes:
                text += latex_greek(child.text)
        elif child.tag == "b":
            text += latex_sc(child.text)
        elif child.tag == "i":
            text += latex_italic(child.text)
        if child.tail is not None:
            text += child.tail
    return text.translate({ord(c): None for c in "\n"})

def parse_ccel_versetable(table):
    text = ""
    for p in table.findall(".//p"):
        text += parse_ccel_paragraph(p) + "\\\\\n"
    return latex_verse(text)


def generate_from_ccel_sites(title, sections, author, sites):
    text = latex_preamble(title, sections, author)
    
    for url, selected_headers in sites:
        all_headers = not any(selected_headers)
        page = requests.get(url)
        root = html.fromstring(page.content)
        for header in root.xpath('//h2'):
            header_text = header.text_content()
            if all_headers or any(string in header_text for string in selected_headers):
                text += latex_section(header_text) + "\n"
                element = header.getnext()
                while element is not None and (element.tag == "p" or element.tag == "table"):
                    if element.tag == "p":
                        text += parse_ccel_paragraph(element) + "\n\n"
                    if element.tag == "table":
                        text += parse_ccel_versetable(element) + "\n"
                    element = element.getnext()

    text += latex_close()
    return text

""" generate_from_ccel_sites((('http://www.ccel.org/ccel/schaff/anf02.v.ii.vi.html', ()),
                         ('http://www.ccel.org/ccel/schaff/anf02.v.ii.vii.html', ()),
                         ('http://www.ccel.org/ccel/schaff/anf02.v.ii.x.html', ())))
"""

