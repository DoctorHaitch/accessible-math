# Accessible Math

A lightweight project exploring **tools, workflows, and best practices for creating accessible mathematics** for the web and assistive technologies.

## Overview

**Accessible Math** is a survey-style project that demonstrates how mathematical content can be authored and delivered in a way that works for **screen readers, braille displays, and other assistive technologies**.

It focuses on the intersection of common math formats (like LaTeX and MathML) and modern web technologies to make math more inclusive.

## Why This Matters

Mathematical notation is inherently visual, which makes it difficult to interpret using assistive tools. Accessibility requires preserving not just how math looks, but its **underlying structure and meaning** so it can be:

- Spoken aloud by screen readers  
- Navigated interactively  
- Converted to braille or other formats  

## Key Topics Covered

This project includes documentation and examples around:

- Math markup languages (LaTeX, MathML)  
- Web rendering tools (e.g., MathJax, DoenetML)  
- Conversion workflows between formats
- Accessible Fonts and Color Palettes for content authoring.

## Future Expansion

I plan to slowly increase content to also include

- Screen reader compatibility  
- Alt text strategies for equations  
- Accessible PDFs and e-books  
- Speech engines and braille output  

The included documentation walks through a **complete workflow for producing accessible math content on the web**.

## Sample Workflow

A typical accessible math workflow demonstrated in this project:

1. Author math and surrounding content in a markup language (e.g., LaTeX, Markdown).
2. Embed math or other manipulatives into an HTML document.
3. Render using a web engine like MathJax, MathML.
4. Ensure semantic structure for assistive technologies.

This hybrid approach balances usability for authors with accessibility for readers.

## Project Structure

```text
.
├── accessible_math_documentation_page.html   # Main documentation page
└── README.md                                # Project overview
```

## Getting Started

To get the project locally:

```bash
git clone https://github.com/DoctorHaitch/accessible-math.git
```

## Technologies Used

- HTML / CSS  
- LaTeX & MathML concepts
- Python and Pandoc

## Contributing

Contributions are welcome! You can help by:

- Adding new tools or workflows  
- Improving documentation  
- Expanding accessibility examples
- Increasing tools discusses such as MathJax/MathQuill for rendering and inputting math  

## License

This project is open-source and available under the repository’s license.
