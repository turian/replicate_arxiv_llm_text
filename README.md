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
        "include_figures": False
    }
)
```

### Input Parameters

- `arxiv_url`: Any arXiv URL format is accepted:
  - Abstract page: `https://arxiv.org/abs/2004.10151`
  - PDF: `https://arxiv.org/pdf/2004.10151.pdf`
  - HTML: `https://arxiv.org/html/2004.10151`
  - ar5iv: `https://ar5iv.org/abs/2004.10151`
- `include_figures`: Boolean, default `False`. Whether to include figure definitions in the output.

### Output

The model returns a single expanded LaTeX file named `[arxiv_id]_expanded.tex` containing the complete paper content with all includes resolved.

## How It Works

1. **URL Processing**: Extracts the arXiv ID from various URL formats.
2. **Source Retrieval**: Downloads the paper's source files (usually a tar.gz archive) from arXiv.
3. **Main File Detection**: Uses smart heuristics to identify the main LaTeX file:
   - Checks for common filenames (main.tex, paper.tex, etc.)
   - Looks for \documentclass declarations
   - Falls back to first .tex file if needed.
4. **LaTeX Expansion**: Uses `latexpand` (installed via `texlive-extra-utils`) to resolve all includes and macros into a single file.
5. **Cleanup**: Handles LaTeX-specific issues like missing .tex extensions in \input commands.

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

---

*Further technical details and troubleshooting steps will be added after resolving current issues.*
