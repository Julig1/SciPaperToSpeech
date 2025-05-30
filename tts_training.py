import re

# Read the content from output_text.txt
with open("input_text.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Step 1: Remove unnecessary line breaks, extra spaces, and text inside parentheses (including the parentheses)
text_no_parentheses = re.sub(r'\s+', ' ', text)  # Replace all whitespace characters (newlines, tabs, etc.) with a single space
text_no_parentheses = re.sub(r'\(.*?\)', '', text_no_parentheses)  # Remove text inside parentheses (including parentheses)

# Step 2: Manually split sentences based on the defined criteria
sentences = []
start_index = 0
for i in range(1, len(text_no_parentheses)):
    if text_no_parentheses[i-1] == '.' and text_no_parentheses[i] == ' ':
        # Check if the last word before the period has more than one letter
        j = i - 2  # Go back to the character before the space
        while j >= 0 and text_no_parentheses[j].isalpha():
            j -= 1
        word_before_dot = text_no_parentheses[j+1:i-1].strip()

        if len(word_before_dot) > 1 and (i + 1 < len(text_no_parentheses) and text_no_parentheses[i+1].isupper()):
            sentences.append(text_no_parentheses[start_index:i+1].strip())  # Add the sentence
            start_index = i+1  # Update the start index for the next sentence

# Step 3: Write the sentences to a new file, each on a new line
with open("restructured_text.txt", "w", encoding="utf-8") as output_file:
    for sentence in sentences:
        output_file.write(sentence + "\n")

# Step 4: Replace commas with ellipses at the very end
with open("restructured_text.txt", "r", encoding="utf-8") as output_file:
    content = output_file.read()

content_with_ellipses = content.replace(',', '...')

# Step 5: Save the final result with commas replaced by ellipses
with open("restructured_text.txt", "w", encoding="utf-8") as output_file:
    output_file.write(content_with_ellipses)

# Print a confirmation message
print("Text has been restructured and saved to restructured_text.txt.")

from gtts import gTTS
import os

# Read the content from restructured_text.txt
with open("restructured_text.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Adjust pauses after commas by replacing commas with a shorter pause (e.g., a space or period for a slight pause)
text = text.replace(",", " ")  # Replace commas with a space (or you can experiment with a few dots like "...")

# Convert the text to speech using gTTS
tts = gTTS(text=text, lang='en', slow=False)

# Save the speech as an MP3 file
tts.save("output_speech.mp3")

# Play the MP3 file (for Windows, replace with 'start' or 'open' based on your OS)
os.system("start output_speech.mp3")
