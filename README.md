# replicate_arxiv_llm_text

A [Replicate](https://replicate.com) model that prepares arXiv papers for processing by Large Language Models (LLMs) by converting them to pure text format.

## Overview

This model takes an arXiv paper URL (in any format - abstract page, PDF, or HTML version) and returns a clean, expanded LaTeX file suitable for LLM processing. It:

1. Downloads the paper's source files from arXiv
2. Identifies the main LaTeX file
3. Expands all includes and macros into a single, self-contained file
4. Optionally includes or excludes figures (disabled by default)

## Usage

You can use this model through the Replicate API or web interface:

```python
import replicate

# Run the model
output = replicate.run(
    "username/replicate_arxiv_llm_text:version",
    input={
        "arxiv_url": "https://arxiv.org/abs/2004.10151",
        "include_figures": False,
        "include_comments": True
    }
)
```

### Testing Locally with `cog predict`

You can test the model locally using the `cog predict` command after building the Docker image:

```bash
cog predict -i arxiv_url="https://arxiv.org/abs/2004.10151" -i include_figures=false -i include_comments=true
```

This command will run the model on the given arXiv paper and output the expanded LaTeX file in your current directory.

### Input Parameters

- `arxiv_url`: Any arXiv URL format is accepted:
  - Abstract page: `https://arxiv.org/abs/2004.10151`
  - PDF: `https://arxiv.org/pdf/2004.10151.pdf`
  - HTML: `https://arxiv.org/html/2004.10151`
  - ar5iv: `https://ar5iv.org/abs/2004.10151`
- `include_figures`: Boolean, default `False`. Whether to include figure definitions in the output.
- `include_comments`: Boolean, default `True`. Whether to include comments in the expanded LaTeX output.

### Output

The model returns a single expanded LaTeX file named `[arxiv_id]_expanded.tex` containing the complete paper content with all includes resolved.

## How It Works

1. **URL Processing**: Extracts the arXiv ID from various URL formats.
2. **Source Retrieval**: Downloads the paper's source files (usually a tar.gz archive) from arXiv.
3. **Main File Detection**: Uses smart heuristics to identify the main LaTeX file:
   - Checks for common filenames (main.tex, paper.tex, etc.)
   - Looks for \documentclass declarations
   - Falls back to first .tex file if needed.
4. **LaTeX Expansion**: Uses `latexpand` (downloaded directly from its repository) to resolve all includes and macros into a single file.
    Since we're not expanding `\usepackage{...}` directives, `latexpand` doesn't require any TeX-related dependencies or `kpsewhich`. It runs solely with Perl, reducing dependencies and simplifying the build process.

### Additional Notes on `latexpand`

- **No TeX Dependencies Required**:

  - `latexpand` typically relies on TeX utilities like `kpsewhich` to locate `.sty` files when expanding `\usepackage{...}` directives.
  - Since we are **not** expanding style files (by avoiding the `--expand-usepackage` option), `latexpand` does **not** require `kpsewhich` or any TeX-related packages.
  - This allows us to run `latexpand` with just Perl installed, simplifying the environment setup.

- **Handling of Comments**:

  - By default, `latexpand` strips comments from the LaTeX files.
  - We've introduced the `include_comments` parameter (default `True`) to control this behavior.
    - When `include_comments` is `True`, the `--keep-comments` option is used, and comments are retained in the output.
    - Users can set `include_comments` to `False` to remove comments if desired.

- **File Inclusion Mechanics**:

  - `latexpand` processes `\input{...}` and `\include{...}` commands, recursively including the contents of the specified files.
  - It uses the current directory (set via the `TEXINPUTS` environment variable) to locate files, which works seamlessly within the extracted arXiv source files.

- **Limitations**:
  
  - **Verbatim Environments**: `latexpand` may not handle content within `\begin{verbatim}...\end{verbatim}` blocks correctly, especially comments or inclusion commands inside these blocks.
  - **Special Macros**: Complex macros or unusual LaTeX constructs may not be expanded as expected.
  - **No Style File Expansion**: Since we're not using `--expand-usepackage`, style files (`.sty`) are not expanded. This is intentional to avoid dependency on TeX packages.

**Polishing for External Consumption**:

- Ensured that explanations are clear and jargon-free for users unfamiliar with `latexpand`.
- Provided context on why we've minimized dependencies and how it benefits users (easier setup, lighter environment).
- Highlighted default behaviors and how users can adjust parameters to fit their needs.

---

## Notes on Interesting Behaviors or Glitches in `latexpand`

After examining `latexpand`, we've identified several behaviors that users should be aware of:

- **Environment Variable `TEXINPUTS`**:

  - `latexpand` uses the `TEXINPUTS` environment variable to locate files for inclusion.
  - By default, if `TEXINPUTS` is not set, it searches in the current directory `.`.
  - In our implementation, this works well because all the necessary files are within the extracted source directory.

- **Comment Handling Nuances**:

  - When comments are stripped (without `--keep-comments`), `latexpand` carefully handles lines ending with `%` to avoid unintended whitespace or concatenation issues.
  - There are special cases where comments inside commands like `\url{...}` can cause issues if they contain unescaped `%` characters.

- **File Not Found Warnings**:

  - If `latexpand` cannot find a file to include, it will print a warning but continue processing.
  - Since we're working within the self-contained source from arXiv, missing files are less likely, but it's something users should be aware of.
  - Using the `--fatal` option would make `latexpand` exit on missing files, but we're not using this to maintain robustness.

- **Limitations with Certain Environments**:

  - `latexpand` doesn't handle the `verbatim` environment and similar environments well, which can lead to unexpected behavior if these environments contain `\input` or `\include` commands.
  - Users should be cautious if their documents heavily use such environments.

---

## Known Issues

- **Environment Variables in `cog.yaml`:**

  The `environment` key is not supported in `cog.yaml`, and using `export` within the `run` section does not persist variables across commands. This can cause issues when environment variables are needed during the build process.

  *Error Message:*

  ```
  There is a problem in your cog.yaml file.
  Additional property environment is not allowed.
  ```

  *Solution:*

  To set environment variables in `cog.yaml`, include them inline at the beginning of each command that requires them.

  **Example:**

  ```yaml
  build:
    run:
      - VAR1=value1 VAR2=value2 command_here arg1 arg2
  ```

  This ensures the environment variables are available for that specific command without relying on `export`.

### Limitations of `latexpand`

While `latexpand` is powerful, there are some known limitations:

- **Verbatim Environments**: `latexpand` may not handle `\begin{verbatim}...\end{verbatim}` blocks correctly, especially concerning comments and included files within verbatim environments.
- **Comments in Verbatim**: Comments inside verbatim environments might be stripped out even when comments are intended to be part of the verbatim text.
- **Processing Commands Inside Verbatim**: `latexpand` might process `\input` and `\include` commands inside verbatim environments, which is usually undesirable.

**Note**: Users should be cautious when processing documents that heavily utilize verbatim or special LaTeX environments. Review the expanded output for any inconsistencies.

---

## Summary of Changes:

- **`cog.yaml`:**

  - Removed all TeX-related installations and environment variables.
  - Only `perl` and `wget` are installed, simplifying dependencies.

- **`predict.py`:**

  - Confirmed that the `include_comments` parameter is already implemented and functioning as intended.

- **`README.md`:**

  - Updated to explain the absence of TeX dependencies and how `latexpand` operates in this context.
  - Added notes on interesting behaviors and limitations of `latexpand`.
  - Polished language and explanations for clarity, targeting users unfamiliar with `latexpand`.

---

By making these changes, we've streamlined our setup by removing unnecessary TeX installations, provided users with control over comment inclusion, documented important behaviors and limitations of `latexpand`, and improved the overall clarity of our documentation for external users.

