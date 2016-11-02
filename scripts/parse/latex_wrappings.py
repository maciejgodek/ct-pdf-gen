def latex_preamble(title, sections, author):
    return r"""\documentclass[9pt, twocolumn, oneside, a4paper]{memoir}
\usepackage{fontspec}
\setmainfont{Alegreya}
\usepackage{ragged2e}
\newfontfamily\scshape{Alegreya SC}
\newfontfamily\headingfont{Alegreya Sans SC}
\newfontfamily\subheadingfont[
    BoldFont={Alegreya Sans Medium},
    ItalicFont={Alegreya Sans Light Italic},
    BoldItalicFont={Alegreya Sans Medium Italic}
]{Alegreya Sans Light}
\newfontfamily\greekfont[Script=Greek, Scale=1.14, WordSpace=0.7]{GFS Neohellenic}
\usepackage{polyglossia}
\setdefaultlanguage{english}
\setotherlanguage[variant=ancient]{greek}
\newcommand{\greektext}[1]{\foreignlanguage{greek}{#1}}

\usepackage{microtype}
\emergencystretch \hsize
\tolerance 300%%
\setlength{\parskip}{0pt}
\frenchspacing

\usepackage{titlesec}
\titleformat*{\section}{\headingfont}

\setlrmarginsandblock{1.37in}{*}{*}
\setulmarginsandblock{1.29in}{*}{2}

\checkandfixthelayout
\setmarginnotes{\columnsep}{0.93in}{0.5\onelineskip}

\pretitle{\par\raggedright\Huge\subheadingfont}
\title{\textit{%s}, %s}
\posttitle{ \textperiodcentered} 
\preauthor{\raggedright\Huge\subheadingfont}
\author{ %s}
\postauthor{\vskip 0.5em}
\predate{}
\date{}
\postdate{}

\newcommand{\gloss}[1]{%%
    \marginpar[\RaggedLeft \footnotesize{#1}]{\RaggedRight \footnotesize{#1}}}

\begin{document}
\maketitle
""" % (title, sections, author)

def latex_close():
    return "\\end{document}"

def latex_section(text):
    return "\\section*{%s}\n" % text

def latex_sc(text):
    return "\\textsc{%s}" % text

def latex_italic(text):
    return "\\textit{%s}" % text

def latex_greek(text):
    return "\\greektext{%s}" % text

def latex_margin(text):
    return "\\gloss{%s}" % text

def latex_footnote(text):
    return "\\footnote{%s}" % text

def latex_verse(text):
    return "\\begin{verse}%s\\end{verse}" % text

def latex_quote(text):
    return "\\begin{quote}%s\\end{quote}" % text

def latex_superscript(text):
    return "\\textsuperscript{%s}" % text
