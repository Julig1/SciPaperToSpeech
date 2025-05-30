# SciPaperToSpeech

SciPaperToSpeech is a Python-based tool that converts LaTeX source code from scientific papers into spoken MP3 files. The program processes LaTeX source code, filters out non-essential elements (such as citations, page numbers, and formatting artifacts), and produces a clean, spoken version of the content using text-to-speech synthesis.

## Overview

Scientific papers often contain structural elements that are irrelevant for audio consumption, such as citations, references, and page numbers. SciPaperToSpeech addresses this issue by converting LaTeX source code into speech while excluding non-essential content. This process ensures that users can listen to the core content of research papers without distractions.

## Features

- Accepts LaTeX source code and processes it into a clean text format.
- Removes unnecessary elements such as:
  - Citation markers and references
  - Page numbers and watermarks
  - Unwanted formatting artifacts
- Segments the cleaned text into well-defined sentences using simple punctuation-based heuristics.
- Replaces commas with ellipses or other pauses for smoother speech synthesis.
- Converts the processed text into audio using Google Text-to-Speech (`gTTS`).
- Outputs an MP3 file for convenient playback.

## Requirements

- Python 3.7 or later
- Dependencies:
  - `gTTS`

Install required packages using pip:

```bash
pip install gTTS
```
## Usage

1. Provide the LaTeX source code of the scientific paper as an input to the program.
2. The program will clean the LaTeX code by removing unwanted sections and formatting.
3. The cleaned text will be converted into speech and saved as an MP3 file.

### Example

```bash
python main.py 
```
After running the script, the following output files will be generated:

restructured_text.txt: Cleaned and restructured text.

output_speech.mp3: Spoken audio of the cleaned text.

The MP3 file can be played using any standard audio player.

## Future Work: arXiv Web Scraping
The program will soon include the capability to automatically retrieve LaTeX source code directly from research papers hosted on arXiv. This will allow users to provide a paper's DOI or URL, and the program will fetch and process the source code automatically.

