# from gtts import gTTS
from moviepy.editor import *
from moviepy.config import change_settings

IMAGEMAGICK_PATH = r'C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe'
change_settings({"IMAGEMAGICK_BINARY": IMAGEMAGICK_PATH})

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

# from PIL import Image, ImageDraw, ImageFont

# Open the input image
# image = Image.open("logo.png").convert("RGBA")
# size = (70,70)
# # Create a mask to create a round image
# mask_size = (min(image.size),) * 2  # make the mask square
# mask = Image.new('L', mask_size, 0)
# draw = ImageDraw.Draw(mask)
# draw.ellipse((0, 0) + mask_size, fill=255)

# # Resize the image to fit the mask size
# image = image.resize(mask_size)

# # Apply the mask to the image
# rounded_image = Image.new('RGBA', mask_size)
# rounded_image.paste(image, (0, 0), mask)

# # Resize the rounded image to the desired size
# rounded_image = rounded_image.resize(size)

# # Save the output image
# rounded_image.save("test.png")



# image = Image.new("RGB", ())











# image_text = Image.open("text.png")


# width = image_text.width + 20 + image_logo.width 
# height = max(image_logo.height, image_text.height)

# image_new = Image.new("RGBA", (width, height), color="white")

# image_new.paste(image_logo, (0, 0))
# image_new.paste(image_text, (image_logo.width + 20, (height - image_text.height) // 2))
# image_new.save("output.png")

# logo = Image.open("test.png")
# rest = Image.open("saved_2.png")

# print(logo.size, rest.size)

# max_h = max(logo.height, rest.height) + 10
# width = logo.width + rest.width

# new = Image.new("RGB", (width, max_h), "WHITE")

# new.paste(logo, (0, 5))
# new.paste(rest, (logo.width + 10, 5))
# new.save("new.png")