# replicate_arxiv_llm_text

[![Replicate](https://img.shields.io/badge/Replicate-arXiv__LLM__Text-blue?logo=Replicate&style=flat-square)](https://replicate.com/turian/arxiv-llm-text)

**Purpose:** Prepare arXiv papers for processing by Large Language Models (LLMs) by converting them into a single, expanded LaTeX file.

This code was written using [Aider](https://aider.chat/).

## Overview

**How It Works:**
- **Input:** An arXiv URL (abstract, PDF, or HTML page).
- **Process:**
  - Downloads and extracts the paper's source files from arXiv.
  - Identifies the main LaTeX file using heuristics.
  - Expands all `\input{}` and `\include{}` commands into a single file using `latexpand`.
  - Optionally includes or excludes comments and figures.
- **Output:** A single, self-contained LaTeX file ready for LLM consumption.

## Usage

You can use this model directly on Replicate:

[https://replicate.com/turian/arxiv-llm-text](https://replicate.com/turian/arxiv-llm-text)

### Input Parameters

- `arxiv_url`: Any arXiv URL format is accepted:
  - Abstract page: `https://arxiv.org/abs/2004.10151`
  - PDF: `https://arxiv.org/pdf/2004.10151.pdf`
  - HTML: `https://arxiv.org/html/2004.10151`
- `include_figures`: Boolean, default `False`. Whether to include figure definitions in the output.
- `include_comments`: Boolean, default `True`. Whether to include comments in the expanded LaTeX output.

## Known Behaviors and Limitations

- **Multiple Main Files Found:**
  - If multiple possible main `.tex` files are found (e.g., several files containing `\documentclass`), the model will **fail** to prevent unintended behavior.
  - **What Happens:**
    - The model raises an error indicating that multiple main files were detected, and it's ambiguous which one to use.
  - **Recommended Action:**
    - Users should ensure their arXiv submission contains a uniquely identifiable main TeX file, typically named `main.tex` or similar.
  - **Note:**
    - The model no longer accepts a `main_file` parameter to specify the main TeX file.

- **Behavior of `latexpand`:**
  - **No TeX Dependencies Required:**
    - `latexpand` runs solely with Perl, without requiring TeX-related packages like `kpsewhich`, since we are not expanding style files.
  - **Comment Handling:**
    - By default, comments are included in the output (`include_comments` parameter is `True`). Users can exclude comments by setting this parameter to `False`.
  - **Limitations:**
    - May not handle `\begin{verbatim}...\end{verbatim}` blocks correctly, especially if they contain comments or inclusion commands.
    - Does not expand `.sty` files or handle complex macros that depend on external style files.

## Notes

- **Glitches in Our Code:**
  - The heuristic for finding the main TeX file may fail if the paper's structure is unconventional.
  - Users may need to adjust their submissions or ensure their arXiv submission contains a uniquely identifiable main TeX file.

- **Glitches in `latexpand`:**
  - Special environments or macros may not be expanded as expected.
  - Files within verbatim environments may be processed incorrectly.

## Output

- The model returns a single expanded LaTeX file named `[arxiv_id]_expanded.tex` containing the complete paper content with all includes resolved.

![arXiv LLM Text Logo](./arxiv_llm_text.webp)
