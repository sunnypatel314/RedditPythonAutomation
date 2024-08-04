# from gtts import gTTS
# from moviepy.editor import *
# from moviepy.config import change_settings

# IMAGEMAGICK_PATH = r'C:\Program Files\ImageMagick-7.1.1-Q16\magick.exe'
# IMAGEMAGICK_PATH = r'C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe'
# change_settings({"IMAGEMAGICK_BINARY": IMAGEMAGICK_PATH})

# # Define the text you want to read
# # text = "Hello, this is a test of the text-to-speech capabilities of Python."

# # # Define the language and create the gTTS object
# # tts = gTTS(text=text, lang='en-uk', tld='co.uk')

# # # Save the audio file
# # tts.save("output.mp3")

# # Run pip install TTS

# import torch
# from TTS.api import TTS

# device = "cuda" if torch.cuda.is_available() else "cpu"
# print(device)

# print(TTS().list_models())

# # First run tts = TTS(model_name='tts_models/multilingual/multi-dataset/xtts_v2').to(device)

# tts = TTS(model_name='tts_models/multilingual/multi-dataset/xtts_v2')

# tts.tts_to_file(text="What up this is the text to speech model yurrr", speaker_wav="harvard.wav", language="en", file_path="output.wav")
# print("Works!")

# Speaker_wav is the voice sample you want to replicate.

from PIL import Image

image = Image.open(fp="images/31415.png")

print(image.size)