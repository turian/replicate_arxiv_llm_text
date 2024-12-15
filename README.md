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

1. **URL Processing**: Extracts the arXiv ID from various URL formats
2. **Source Retrieval**: Downloads the paper's source files (usually a tar.gz archive) from arXiv
3. **Main File Detection**: Uses smart heuristics to identify the main LaTeX file:
   - Checks for common filenames (main.tex, paper.tex, etc.)
   - Looks for \documentclass declarations
   - Falls back to first .tex file if needed
4. **LaTeX Expansion**: Uses `latexpand` to resolve all includes and macros into a single file
5. **Cleanup**: Handles LaTeX-specific issues like missing .tex extensions in \input commands

## Use Cases

This model is particularly useful for:
- Preparing arXiv papers for LLM training
- Creating clean text versions of papers for analysis
- Extracting paper content without PDF conversion artifacts
- Batch processing of academic papers

## Technical Details

Built using:
- [Cog](https://github.com/replicate/cog)
- Python's `arxiv` package for source retrieval
- `latexpand` for LaTeX processing
- Minimal texlive installation for LaTeX handling

### Package Installation Notes

The model requires `latexpand` which is provided by the `texlive-extra-utils` package. Getting the right combination of TeX packages installed was challenging:

1. Initial attempts:
   - `texlive-latex-recommended` alone: Missing `latexpand`
   - `texlive-binaries`: Basic TeX tools but no `latexpand`
   - Full `texlive` installation: Too large, caused build timeouts

2. Issues encountered:
   - Format building failures during tex-common configuration
   - Dependency conflicts between TeX packages
   - Missing format files causing post-installation errors

3. Working solution:
   - Minimal set: `texlive-base`, `texlive-binaries`, `texlive-extra-utils`
   - Removed `texlive-latex-recommended` to avoid format building issues
   - Order of installation matters to prevent dependency conflicts

If you encounter "fmtutil failed" errors or "tex-common configuration failed", try:
- Ensuring sufficient disk space and memory for format building
- Installing packages in correct dependency order
- Using minimal TeX installation to avoid format building complexity

## Limitations

- Requires papers to have source files available on arXiv
- Some extremely complex LaTeX setups might need manual intervention
- Custom class files or unusual package usage might affect expansion
- Figure inclusion is basic and might not handle all cases perfectly

## License

Apache 2.0

## Development

### Local Testing

1. Install Cog:
```bash
curl -o /usr/local/bin/cog -L https://github.com/replicate/cog/releases/latest/download/cog_`uname -s`_`uname -m`
chmod +x /usr/local/bin/cog
```

2. Build the model:
```bash
cog build
```

3. Test the model locally:
```bash
cog predict -i arxiv_url="https://arxiv.org/abs/2004.10151"
```

### Deployment

1. Log in to Replicate:
```bash
cog login
```

2. Push the model:
```bash
cog push r8.im/username/replicate_arxiv_llm_text
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
