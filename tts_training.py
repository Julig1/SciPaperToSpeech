import os
import re
import tarfile
import tempfile
from pathlib import Path
from gtts import gTTS
from pylatexenc.latex2text import LatexNodes2Text
from tqdm import tqdm  # Import tqdm for the progress bar
import time

# === TAR PROCESSING ===

def find_tarball():
    tar_files = [f for f in os.listdir('.') if f.endswith('.tar.gz')]
    if len(tar_files) == 0:
        raise FileNotFoundError("No .tar.gz file found in the current directory.")
    elif len(tar_files) > 1:
        raise FileExistsError("Multiple .tar.gz files found. Please keep only one.")
    return tar_files[0]

def extract_tarball(tar_path):
    temp_dir = tempfile.mkdtemp()
    with tarfile.open(tar_path, "r:gz") as tf:
        tf.extractall(path=temp_dir)
    return temp_dir

def find_main_tex_file(extract_path):
    tex_files = list(Path(extract_path).rglob("*.tex"))
    if not tex_files:
        raise FileNotFoundError("No .tex files found in extracted contents.")
    main_tex = max(tex_files, key=lambda f: f.stat().st_size)
    return main_tex

# === LATEX CLEANING ===

def clean_latex_text(latex_str):
    match = re.search(r'(\\(section|subsection)\{)', latex_str)
    if match:
        latex_str = latex_str[match.start():]

    latex_str = re.split(r'\\(bibliography|begin\{thebibliography\})', latex_str)[0]

    latex_str = re.sub(r'%.*', '', latex_str)
    latex_str = re.sub(r'\\cite[t|p]?(\[[^\]]*\])?(\{[^\}]*\})', '', latex_str)
    latex_str = re.sub(r'\[\d+(,\s*\d+)*\]', '', latex_str)
    latex_str = re.sub(r'\\ref\{[^\}]*\}', '', latex_str)
    latex_str = re.sub(r'\\footnote\{.*?\}', '', latex_str)

    text = LatexNodes2Text().latex_to_text(latex_str)
    return ' '.join(text.split())

# === LOCAL EXTRACTIVE SUMMARY ===

def extract_summary(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    summary_sents = [s for s in sentences if len(s.split()) > 8][:2]
    return ' '.join(summary_sents)

# === TEXT TO SPEECH ===

def text_to_speech(text, out_path="output.mp3"):
    sentences = text.split('. ')
    total_sentences = len(sentences)
    
    # Combine sentences into larger chunks to reduce the number of calls to gTTS
    max_sentences_per_chunk = 5  # Generate speech for larger chunks (5 sentences at once)
    chunks = [". ".join(sentences[i:i + max_sentences_per_chunk]) for i in range(0, total_sentences, max_sentences_per_chunk)]

    # Set up a progress bar
    with tqdm(total=len(chunks), desc="Generating speech...", ncols=100) as pbar:
        full_text = ""
        for chunk in chunks:
            full_text += chunk + ". "
            attempt = 0
            while attempt < 3:
                try:
                    # Only generate the speech once for each chunk
                    tts = gTTS(full_text, lang='en')
                    tts.save(out_path)
                    pbar.update(1)  # Update progress bar after each chunk
                    break
                except Exception as e:
                    print(f"Error generating speech: {e}")
                    if '429' in str(e):  # If rate limit error
                        print("Rate limit exceeded, retrying...")
                        time.sleep(10)  # Wait for 10 seconds before retrying
                    else:
                        break  # If the error is not rate limit, break out of retry loop
                    attempt += 1
            else:
                print("Failed to generate speech after multiple attempts.")
                break  # Break out of loop after retries are exhausted
        print(f"Speech saved to: {out_path}")

# === MAIN FUNCTION ===

def main():
    try:
        tar_file = find_tarball()
        print(f"Found tarball: {tar_file}")

        extract_path = extract_tarball(tar_file)
        print(f"Extracted to: {extract_path}")

        main_tex_path = find_main_tex_file(extract_path)
        print(f"Using main .tex file: {main_tex_path}")

        with open(main_tex_path, 'r', encoding='utf-8') as f:
            latex_str = f.read()

        print("Cleaning LaTeX content...")
        main_text = clean_latex_text(latex_str)

        print("Extracting summary...")
        summary = extract_summary(main_text)
        intro = f"Title and Summary:\n{summary}\n\n🎧 Now the main text begins.\n\n"
        full_text = intro + main_text

        print("Converting to speech...")
        text_to_speech(full_text)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
