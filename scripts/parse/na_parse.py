
from lxml import html
import requests
from parse.latex_wrappings import *

def parse_nadv_emph(em):
    return latex_italic(parse_nadv_paragraph(em))

def parse_nadv_footnote(span):
    return latex_margin(parse_nadv_paragraph(span))

def parse_nadv_blockquote(blockquote):
    text = ""
    if len(blockquote.findall(".//p")) == 1:
        return latex_quote(parse_nadv_paragraph(blockquote.find(".//p"))) 
    for p in blockquote.findall(".//p"):
        text += "\n" + parse_nadv_paragraph(p) + "\n"
    return text

def parse_nadv_paragraph(p):
    text = ""
    if p.text is not None:
        text += p.text
    for child in p:
        if child.text is not None:
            if child.tag == "a":
                text += parse_nadv_paragraph(child)
            if child.tag == "strong":
                text += latex_sc(child.text)
            if child.tag == "em":
                text += parse_nadv_emph(child)
        if child.tag == "q":
            text += "``" + parse_nadv_paragraph(child) + "''"
        if child.tag == "span" and "stiki" in child.classes:
            text += parse_nadv_footnote(child)
        if child.tag == "span" and "greek" in child.classes:
            text += latex_greek(child.text)
        if child.tail is not None:
            text += child.tail
    return text.translate({ord(c): None for c in "\n"})

def generate_from_nadv_sites(title, sections, author, sites):
    text = latex_preamble(title, sections, author)
    
    for url, selected_headers in sites:
        all_headers = not any(selected_headers)
        page = requests.get(url)
        root = html.fromstring(page.content)
        for header in root.xpath("//h2"):
            header_text = header.text_content()
            if (all_headers or any(string in header_text for string in selected_headers)) and not "About this page" in header_text:
                text += latex_section(header_text) + "\n"
                element = header.getnext()
                while element is not None and (element.tag == "p" or element.tag == "blockquote"):
                    if element.tag == "p":
                        text += "\n" + parse_nadv_paragraph(element) + "\n"
                    if element.tag == "blockquote":
                        text += parse_nadv_blockquote(element)
                    element = element.getnext()

    text += latex_close()
    return text


# sites = (("http://www.newadvent.org/fathers/020801.htm", ()), )

# print(generate_from_nadv_sites("Exhortation to the Heathen", "ch.1", "Clement of Alexandria", sites))
