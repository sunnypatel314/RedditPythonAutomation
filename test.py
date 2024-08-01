from gtts import gTTS
from moviepy.editor import *
from moviepy.config import change_settings
from PIL import Image

IMAGEMAGICK_PATH = r'C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe'
change_settings({"IMAGEMAGICK_BINARY": IMAGEMAGICK_PATH})

# Define the text you want to read
# text = "Hello, this is a test of the text-to-speech capabilities of Python."

# # Define the language and create the gTTS object
# tts = gTTS(text=text, lang='en-uk', tld='co.uk')

# # Save the audio file
# tts.save("output.mp3")

