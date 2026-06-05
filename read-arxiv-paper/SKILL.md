---
name: read-arxiv-paper
description: Use this skill when asked to read an arxiv paper given an arxiv URL
---

You will be given a URL of an arxiv paper, for example:

https://www.arxiv.org/abs/2601.07372

### Part 1: Normalize the URL

The goal is to fetch the TeX Source of the paper (not the PDF!), the URL always looks like this:

https://www.arxiv.org/src/2601.07372

Notice the /src/ in the url. Once you have the URL:

### Part 2: Download the paper source

Fetch the url to a local .tar.gz file. A good location is `~/.cache/read_arxiv_paper/knowledge/{arxiv_id}.tar.gz`.

(If the file already exists, there is no need to re-download it).

### Part 3: Unpack the file in that folder

Unpack the contents into `~/.cache/read_arxiv_paper/knowledge/{arxiv_id}` directory.

### Part 4: Locate the entrypoint

Every latex source usually has an entrypoint, such as `main.tex` or something like that.

### Part 5: Read the paper

Once you've found the entrypoint, Read the contents and then recurse through all other relevant source files to read the paper.

### Part 6: Report

Once you've read the paper, write a detailed, reader-friendly Markdown introduction based on the paper source files in this directory.

Requirements:

- Output language: Chinese (professional terms may remain in English).
- Content depth: explain the paper in detail using simple, easy-to-understand language.
- Visuals: make it illustrated with figures from the paper; use relative paths to local image files; do not reference PDF pages; prefer png/jpeg image files. If host machine is missing image processing tools, just use the raw image files.
- Formulas: ensure all formulas render correctly with KaTeX (Feishu-compatible).
- Important formula rule: to avoid parsing errors, never use `<` directly in formulas; replace it with `\\lt` (for example, write `_{\\lt t}`).
- Structure: if possible, include pseudocode at the end.
- Markdown quality: must be Typora-compatible, complete, and well-rendered (for example, keep spaces around bold markers when needed).
- Output file path: must save the final document as `~/.cache/read_arxiv_paper/knowledge/paper_reading.md` in the current directory.

### Part 7: Send to User
If you have access to Feishu, please also send the generated `paper_reading.md` file to the feishu-docs
If you have access to ima skills, please upload the generated `paper_reading.md` file to the ima docs with name `{arxiv_id}.md` in proper folder.
