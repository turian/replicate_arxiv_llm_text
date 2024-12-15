import os
import re
import subprocess
import tempfile
from urllib.parse import urlparse

import arxiv
import requests
from bs4 import BeautifulSoup
from cog import BasePredictor, Input, Path


class Predictor(BasePredictor):
    def setup(self):
        """Setup runs once when the model is loaded"""
        # Check if latexpand is available
        try:
            subprocess.run(["which", "latexpand"], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            raise RuntimeError("latexpand not found. Please install texlive-extra-utils")

    def extract_arxiv_id(self, url):
        """Extract arXiv ID from various URL formats"""
        # Handle different URL patterns
        patterns = [
            r"arxiv.org/abs/(\d+\.\d+)",
            r"arxiv.org/pdf/(\d+\.\d+)",
            r"ar5iv.org/abs/(\d+\.\d+)",
            r"arxiv.org/html/(\d+\.\d+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        raise ValueError("Could not extract arXiv ID from URL")

    def find_main_tex_file(self, directory):
        """Find the main TeX file using heuristics similar to arXiv"""
        tex_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".tex"):
                    tex_files.append(os.path.join(root, file))

        if not tex_files:
            raise ValueError("No .tex files found")

        # Heuristics to find main file:
        # 1. Look for common main file names
        common_names = ["main.tex", "paper.tex", "ms.tex", "manuscript.tex"]
        for name in common_names:
            if name in [os.path.basename(f) for f in tex_files]:
                return next(f for f in tex_files if os.path.basename(f) == name)

        # 2. Look for file with \documentclass
        for tex_file in tex_files:
            with open(tex_file, "r", encoding="utf-8") as f:
                content = f.read()
                if "\\documentclass" in content:
                    return tex_file

        # 3. If all else fails, take the first .tex file
        return tex_files[0]

    def predict(
        self,
        arxiv_url: str = Input(description="arXiv URL (abs/pdf/html)"),
        include_figures: bool = Input(
            description="Include figure files in expansion", default=False
        ),
    ) -> Path:
        """Run prediction on an arXiv paper"""
        # Extract arXiv ID
        arxiv_id = self.extract_arxiv_id(arxiv_url)

        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Download source using arxiv API
            paper = next(arxiv.Search(id_list=[arxiv_id]).results())
            source_url = paper.entry_id.replace("/abs/", "/e-print/")

            # Download and extract source
            response = requests.get(source_url)
            archive_path = os.path.join(temp_dir, "source.tar.gz")
            with open(archive_path, "wb") as f:
                f.write(response.content)

            # Extract archive
            extract_dir = os.path.join(temp_dir, "extracted")
            os.makedirs(extract_dir)
            subprocess.run(["tar", "xf", archive_path, "-C", extract_dir], check=True)

            # Find main TeX file
            main_tex = self.find_main_tex_file(extract_dir)

            # Process input files to add .tex extensions
            with open(main_tex, "r", encoding="utf-8") as f:
                content = f.read()
            processed_content = re.sub(r"\\input{([^}]*)}", r"\\input{\1.tex}", content)

            processed_tex = os.path.join(temp_dir, "processed_main.tex")
            with open(processed_tex, "w", encoding="utf-8") as f:
                f.write(processed_content)

            # Run latexpand
            output_path = os.path.join(temp_dir, "expanded.tex")
            cmd = ["latexpand"]
            if not include_figures:
                cmd.append("--empty-comments")
            cmd.extend(["--keep-comments", processed_tex])

            with open(output_path, "w") as f:
                subprocess.run(cmd, stdout=f, check=True)

            # Copy to output directory
            output_dir = Path(os.getcwd())
            final_path = output_dir / f"{arxiv_id}_expanded.tex"
            subprocess.run(["cp", output_path, str(final_path)], check=True)

            return final_path
