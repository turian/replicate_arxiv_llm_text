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

### Fixing the `cog.yaml` Error and Documenting in `README.md`

---

#### Fixing the `cog.yaml` Environment Variable Issue

We encountered an issue when building the Docker image using Cog. The error was:

```
There is a problem in your cog.yaml file.
Additional property environment is not allowed.

To see what options you can use, take a look at the docs:
https://github.com/replicate/cog/blob/main/docs/yaml.md

You might also need to upgrade Cog, if this option was added in a
later version of Cog.
```

**Explanation:**

- The `environment` key is **not supported** in `cog.yaml` according to the [Cog documentation](https://github.com/replicate/cog/blob/main/docs/yaml.md).
- Attempting to use it results in the error about an additional property not being allowed.

**What We Tried:**

- We initially added an `environment` section in `cog.yaml` to set environment variables globally during the build process.
- This led to the build error mentioned above.

**Solution:**

- Removed the unsupported `environment` key from `cog.yaml`.
- Moved the setting of environment variables into the `run` section to ensure they are available during the build commands.
- Consolidated relevant commands into a single multi-line `run` block to maintain the environment variables throughout the build process.

**Updated `cog.yaml` Snippet:**

```yaml
build:
  gpu: false
  python_version: '3.11'
  run:
    - |
      # Set environment variables and create directories
      export MKTEXLSR=no
      export TEXMFVAR=/tmp/texmf-var
      export TEXMFCONFIG=/tmp/texmf-config
      export HOMETEXMF=/tmp/texmf-home
      mkdir -p $TEXMFVAR $TEXMFCONFIG $HOMETEXMF

      apt-get update -qq

      # Install minimal necessary packages without recommends
      DEBIAN_FRONTEND=noninteractive \
      apt-get install -y --no-install-recommends wget perl texlive-latex-base texlive-binaries

      # Manually download latexpand
      wget -O /usr/local/bin/latexpand https://raw.githubusercontent.com/latex3/latex3/master/tools/latexpand/latexpand
      chmod +x /usr/local/bin/latexpand

      rm -rf /var/lib/apt/lists/*

  python_packages:
    - requests
    - beautifulsoup4
    - arxiv

predict: predict.py:Predictor
```

**Benefits of This Approach:**

- **Compliance with `cog.yaml` Specifications:**
  - Avoids using unsupported keys, preventing build errors.
- **Proper Environment Variable Handling:**
  - Ensures environment variables are set when needed by grouping commands.
- **Clean and Manageable Build Steps:**
  - Consolidates related commands for better readability and maintenance.

---

### **Updated `README.md`:**

Under the **Technical Details** or **Troubleshooting** section, add the following to document what was tried and how the issue was resolved:

---

#### Fixing the `cog.yaml` Environment Variable Issue

We encountered an issue when building the Docker image using Cog. The error was:

```
There is a problem in your cog.yaml file.
Additional property environment is not allowed.

To see what options you can use, take a look at the docs:
https://github.com/replicate/cog/blob/main/docs/yaml.md

You might also need to upgrade Cog, if this option was added in a
later version of Cog.
```

**Explanation:**

- The `environment` key is **not supported** in `cog.yaml` according to the [Cog documentation](https://github.com/replicate/cog/blob/main/docs/yaml.md).
- Attempting to use it results in the error about an additional property not being allowed.

**What We Tried:**

- We initially added an `environment` section in `cog.yaml` to set environment variables globally during the build process.
- This led to the build error mentioned above.

**Solution:**

- Removed the unsupported `environment` key from `cog.yaml`.
- Moved the setting of environment variables into the `run` section to ensure they are available during the build commands.
- Consolidated relevant commands into a single multi-line `run` block to maintain the environment variables throughout the build process.

**Updated `cog.yaml` Snippet:**

```yaml
build:
  gpu: false
  python_version: '3.11'
  run:
    - |
      # Set environment variables and create directories
      export MKTEXLSR=no
      export TEXMFVAR=/tmp/texmf-var
      export TEXMFCONFIG=/tmp/texmf-config
      export HOMETEXMF=/tmp/texmf-home
      mkdir -p $TEXMFVAR $TEXMFCONFIG $HOMETEXMF

      apt-get update -qq

      # Install minimal necessary packages without recommends
      DEBIAN_FRONTEND=noninteractive \
      apt-get install -y --no-install-recommends wget perl texlive-latex-base texlive-binaries

      # Manually download latexpand
      wget -O /usr/local/bin/latexpand https://raw.githubusercontent.com/latex3/latex3/master/tools/latexpand/latexpand
      chmod +x /usr/local/bin/latexpand

      rm -rf /var/lib/apt/lists/*

  python_packages:
    - requests
    - beautifulsoup4
    - arxiv

predict: predict.py:Predictor
```

**Explanation of Changes:**

- **Removed the `environment` Key:**
  - The `environment` key is not allowed in `cog.yaml`, so we removed it.
- **Used a Multi-Line Command in `run`:**
  - By using `|`, we started a multi-line block where all commands run in the same shell session.
- **Set Environment Variables Within the Shell Session:**
  - Used `export` to set environment variables.
  - These variables are available to subsequent commands within the same `run` block.
- **Used Variables During Package Installation:**
  - Environment variables are set when the `apt-get install` command is executed.

**Next Steps:**

1. **Update `README.md`:**
   - Include the above documentation to inform future developers of the issue and its resolution.

2. **Update `cog.yaml`:**
   - Replace your current `cog.yaml` with the updated version above.

3. **Rebuild the Docker Image:**
   - Run `cog build` to build the image with the corrected `cog.yaml`.

4. **Test the Model:**
   - Use `cog predict` to ensure everything works as expected.

     ```bash
     cog predict -i arxiv_url="https://arxiv.org/abs/2004.10151"
     ```

---

**Summary:**

- **Issue:** The `environment` key is not allowed in `cog.yaml`, causing a build error.
- **Resolution:** Removed the `environment` key and set environment variables within a multi-line `run` block.
- **Documentation:** Updated `README.md` to document the issue, what was tried, and how it was resolved.
- **Action:** Apply the changes to both `README.md` and `cog.yaml`, and rebuild the image.

---

### **Updated `cog.yaml` to Fix the Bug:**

Modify your `cog.yaml` as follows:

```yaml
build:
  gpu: false
  python_version: '3.11'
  run:
    - |
      # Set environment variables and create directories
      export MKTEXLSR=no
      export TEXMFVAR=/tmp/texmf-var
      export TEXMFCONFIG=/tmp/texmf-config
      export HOMETEXMF=/tmp/texmf-home
      mkdir -p $TEXMFVAR $TEXMFCONFIG $HOMETEXMF

      apt-get update -qq

      # Install minimal necessary packages without recommends
      DEBIAN_FRONTEND=noninteractive \
      apt-get install -y --no-install-recommends wget perl texlive-latex-base texlive-binaries

      # Manually download latexpand
      wget -O /usr/local/bin/latexpand https://raw.githubusercontent.com/latex3/latex3/master/tools/latexpand/latexpand
      chmod +x /usr/local/bin/latexpand

      rm -rf /var/lib/apt/lists/*

  python_packages:
    - requests
    - beautifulsoup4
    - arxiv

predict: predict.py:Predictor
```

**Explanation of Changes:**

- **Removed the `environment` Key:**
  - The `environment` key is not allowed in `cog.yaml`, so we removed it.
- **Used a Multi-Line Command in `run`:**
  - By using `|`, we started a multi-line block where all commands run in the same shell session.
- **Set Environment Variables Within the Shell Session:**
  - Used `export` to set environment variables.
  - These variables are available to subsequent commands within the same `run` block.
- **Used Variables During Package Installation:**
  - Environment variables are set when the `apt-get install` command is executed.

**Next Steps:**

1. **Update `README.md`:**
   - Include the above documentation to inform future developers of the issue and its resolution.

2. **Update `cog.yaml`:**
   - Replace your current `cog.yaml` with the updated version above.

3. **Rebuild the Docker Image:**
   - Run `cog build` to build the image with the corrected `cog.yaml`.

4. **Test the Model:**
   - Use `cog predict` to ensure everything works as expected.

     ```bash
     cog predict -i arxiv_url="https://arxiv.org/abs/2004.10151"
     ```

---

Let me know if you have any questions or need further assistance!