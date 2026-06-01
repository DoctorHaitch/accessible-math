# Digital Accessibility in LaTeX Documents  
## Markdown Quickstart Guide (Version 0.2)
## Last updated 4/25/2026

**Author:** Kris Hollingsworth, PhD  

---

## Table of Contents
- [Introduction](#introduction)
- [Software Requirements](#software-requirements)
- [Document Requirements](#document-requirements)
  - [Automatically Tagging Your PDF](#automatically-tagging-your-pdf)
  - [Heading Structure](#heading-structure)
  - [Floating Elements](#floating-elements)
  - [Tables](#tables)
  - [Images and Alt Text](#images-and-alt-text)
  - [Codeblocks](#codeblocks)
- [Known Problematic Packages](#known-problematic-packages)
- [Summary](#summary)
- [List of Class Files](#list-of-class-files)
---

## Introduction

### Federal Accessibility Requirements

Recent updates to federal accessibility regulations under **Title II of the ADA** require digital content produced by public institutions to meet **WCAG 2.1 Level AA** standards.

For academic environments, this means:

- Accessibility must be built-in, not retrofitted  
- Materials must support:
  - Proper document structure  
  - Logical reading order  
  - Alternative text for images  
  - Navigable tables  
  - Compatibility with assistive technologies  

Compliance Deadline: April 24, 2027 (Recently extended from the original 2026 deadline.)

---

## Software Requirements

- [TeX Live 2025+](https://www.tug.org/texlive/)
- [LuaLaTeX compiler](https://www.luatex.org/)

---

## Document Requirements

### Automatically Tagging Your PDF

    \DocumentMetadata{
      tagging=on,
      pdfstandard=ua-2,
      lang=en-US,
      testphase={phase-III,math,table}
    }
    \documentclass[12pt,a4paper]{article}

    \usepackage[
      pdfauthor={Author Name},
      pdftitle={Document Title}
    ]{hyperref}

Note:
- ```\title{}``` and ```\author{}``` do not set PDF metadata  
- ```hyperref``` is required for this.

---

### Heading Structure

    \section{}        %H1 Heading
    \subsection{}     %H2 Heading
    \subsubsection{}  %H3 Heading
    \paragraph{}      %H4 Heading
    \subparagraph{}   %H5 Heading

Note:
- Headings need to be properly nested.
- i.e., don't place a paragraph (H4) directly inside a section (H1).

---

### Floating Elements
    \usepackage{float} %% Add to Preamble, required for [H] tags.

    \begin{figure}[H]
    \caption{Insert Caption}
    \end{figure}
    \begin{table}[H]
    \caption{Insert Caption}
    \end{figure}

Note: 
- [H] tag is required for logical document flow, tables and images should appear in the same order as the document and PDF Stream.
- Including captions is recommended.
---

### Tables
    %% Sets first row as default for table header.
    \tagpdfsetup{table/header-rows={1}}
Note:
- Headings are required for tables.
- Can be used locally as well.
---

### Images and Alt Text
    %% Use built in key.
    \includegraphics{filename}[alt={Sample alternative text.}]
    \begin{tikzpicture}[alt={Sample alternative text.}]
Note:
- Use built-in ```alt``` key for both includegraphics and tikz.
---

### Codeblocks
The following is a useful replacement of the ```listings``` package, which completely breaks page reading order.

    \usepackage{fancyvrb}
    \fvset{
      numbers=left,
      stepnumber=1,
      numbersep=3pt,
      frame=single
    }
    \renewcommand{\theFancyVerbLine}{\footnotesize\arabic{FancyVerbLine}}

---
## Known Problematic Packages

### High Risk (Structure Altering)
- ```titlesec```
- ```sectsty```
- Any structural redifinitions of the heading tags.
- Any templates not specifically designed for accessibility.
- Legacy font packages such as ```mathptmx``` or ```palatino```
- Older encoding packages such as ```fontenc``` or ```inputenc```

### Medium Risk (Compilation Errors or Broken Reading Order)
- ```multicol```
- ```wrapfig```
- ```floatrow```
- ```capt-of```
- ```clerref```
- Reliance on manual box manipulation (```\hbox```, ```\vbox```) (This is one reason the gradetable does not work in the standard exam class with PDFtagging support enabled)
- ```enumitem``` interferes with list tagging, but only causes issues when you attempt to use individual list options. Can redefine labels manually
<!-- -->
    %% Change first level enumerate to arabic numerals. (Default behavior)
    \renewcommand{\labelenumi}{(\arabic{enumi})} 
    %% Change first level enumerate to lower case alpha.
    \renewcommand{\labelenumi}{(\alph{enumi})}  
    %% Change first level enumerate to upper case alpha.
    \renewcommand{\labelenumi}{(\Alph{enumi})}  
    %% Change first level enumerate to lower case roman.
    \renewcommand{\labelenumi}{(\roman{enumi})} 
    %% Change first level enumerate to upper case roman.
    \renewcommand{\labelenumi}{(\Roman{enumi})} 
<!-- -->
- ```natbib``` or heavily customized ```biblatex``` configurations.
- ```listings``` (recommend using fancyvrb)
### Low Risk Graphics and Diagram Packages (Broken Reading Order)
- ```tikz```
- ```pgfplots```
- ```pgf```
- ```asymptote```

## Summary

- Many incompatibilities do not cause compilation errors but instead result in degraded reading order or incomplete tagging.
- Always validate output using a PDF accessibility checker when possible. I recommend the list view in Adobe Acrobat for documents created in LaTeX, as the visual density of tags can become overwhelming with labels, links, math, and other technical environments each creating their own tags.

## List of Class Files

In Progress: accessibleexam.cls, an exam template designed to meet PDF/UA compliance.
