"""
Setup script for Instagram Reel Transcription Tool
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding='utf-8') if readme_path.exists() else ""

setup(
    name="insta-transcriber",
    version="1.0.0",
    author="Your Name",
    description="Transcribe speech from Instagram Reels to text using AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/InstaTranscriber",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "yt-dlp>=2024.1.0",
        "openai-whisper>=20231117",
        "validators>=0.22.0",
        "requests>=2.31.0",
        "tqdm>=4.66.0",
    ],
    entry_points={
        'console_scripts': [
            'insta-transcriber=src.main:main',
        ],
    },
    include_package_data=True,
)
