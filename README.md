# SciPaperToSpeech

SciPaperToSpeech is a Python-based tool that converts LaTeX-generated scientific papers into audio files (MP3 format). It extracts structured text from PDFs, filters out non-essential content such as page numbers, watermarks, citations, and formatting artifacts, and produces a streamlined spoken version of the paper using text-to-speech synthesis.

## Overview

Scientific papers often contain structural elements that are unnecessary or distracting when converted to speech, such as citation markers, excessive whitespace, or layout metadata. SciPaperToSpeech automates the extraction, cleaning, and conversion of such documents into audio while preserving the logical and grammatical structure of the original content.

## Features

- Extracts textual content from LaTeX-based PDF documents using `pdfplumber`
- Cleans and restructures the text to remove:
  - Citation markers and parenthetical notes
  - Page headers, footers, and numbers
  - Formatting irregularities such as line breaks and excess spacing
- Identifies sentence boundaries using basic punctuation and capitalization heuristics
- Replaces commas with ellipses or pauses to improve spoken delivery
- Uses `gTTS` (Google Text-to-Speech) to synthesize natural-sounding audio
- Outputs a playable MP3 file

## Requirements

- Python 3.7 or later
- Dependencies:
  - `pdfplumber`
  - `gTTS`

Install required packages using pip:

```bash
pip install pdfplumber gTTS
