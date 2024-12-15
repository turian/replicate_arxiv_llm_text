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
4. **LaTeX Expansion**: Uses `latexpand` (downloaded directly from its repository) to resolve all includes and macros into a single file. Since we're not expanding `\usepackage{...}` directives, `latexpand` doesn't require `kpsewhich`, reducing dependencies and simplifying the build process.
5. **Cleanup**: Handles LaTeX-specific issues like missing .tex extensions in \input commands.

### Additional Notes on `latexpand`

- **Behavior with Style Files (`.sty`):**

  Since we're not expanding style files by avoiding `--expand-usepackage`, `latexpand` doesn't need to locate `.sty` files, eliminating the need for `kpsewhich`.

- **Handling of Comments:**

  By default, `latexpand` strips comments unless the `--keep-comments` option is used. We've added the `include_comments` parameter to control this behavior, giving users flexibility.

- **Known Glitches or Interesting Behaviors:**

  - **Environment Variable `TEXINPUTS`:** `latexpand` uses the `TEXINPUTS` environment variable to locate LaTeX files. In our use case, we rely on the current directory, simplifying file resolution.
  - **Importance of `--empty-comments`:** When `include_figures` is `False`, we use `--empty-comments` to handle comments correctly without including figure definitions.

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
*Further technical details and troubleshooting steps will be added after resolving current issues.*
