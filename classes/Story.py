import pyttsx3
import os
import librosa
import random
import torch
import whisper_timestamped as whisper
from pydub import AudioSegment
from moviepy.editor import *
from moviepy.config import change_settings
from PIL import Image
from utils.captions import condense_captions

class Story():
    def __init__(self) -> None:
        self.post_title = ""
        self.submission_self_text = ""
        self.post_url = ""
        self.post_id = ""
        self.post_author = ""
        self.audio_file_path = ""
        self.video_file_path = ""
        self.image_file_path = ""
        self.font_path = "Arial-Bold"

        IMAGEMAGICK_PATH = r'C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe'
        change_settings({"IMAGEMAGICK_BINARY": IMAGEMAGICK_PATH})

    def set_post_id(self, id):
        self.post_id = id
        self.audio_file_path = f"audio/{id}.mp3"
        self.video_file_path = f"videos/{id}.mp4"
        self.image_file_path = f"images/{id}.png"

    def set_post_title(self, title):
        self.post_title = title

    def set_post_author(self, author):
        self.post_author = author

    def set_submission_self_text(self, text):
        self.submission_self_text = text

    def set_post_url(self, post_url):
        self.post_url = post_url
    
    def set_font_path(self, font_path):
        self.font_path = font_path

    def create_voiceover(self):
        if not self.audio_file_path or not self.submission_self_text:
            return
        
        def voice_over(text, output, rate_multipler, gender=0):
            engine = pyttsx3.init()
            voices = engine.getProperty("voices")
            rate = engine.getProperty("rate")
            volume = engine.getProperty("volume")
            engine.setProperty("voice", voices[gender].id)
            engine.setProperty("rate", rate * rate_multipler)
            engine.setProperty("volume", volume * 1.1)
            engine.save_to_file(text, output)
            engine.runAndWait()

        voice_over(self.post_title, "title.mp3", 0.97, gender=1)       
        voice_over(self.submission_self_text, "body.mp3", 0.97, gender=1)
        
        audio_title = AudioSegment.from_file("title.mp3")
        audio_body = AudioSegment.from_file("body.mp3")

        silent_pause = AudioSegment.silent(duration=150)
        silent_pause_start = AudioSegment.silent(duration=300)

        combined = silent_pause_start + audio_title + silent_pause + audio_body
        combined.export(self.audio_file_path, format="mp3")
        
    def create_video(self):
        if not self.audio_file_path or not self.video_file_path:
            return 
        
        game = "minecraft"
        GAMEPLAY_FILE_PATH = f"background/{game}.mp4"
        GAMEPLAY_DURATION = int(VideoFileClip(GAMEPLAY_FILE_PATH).duration)

        audio_duration = int(librosa.get_duration(path=self.audio_file_path)) + 1
        if audio_duration > GAMEPLAY_DURATION:
            print("The story is too long.")
            return
        if audio_duration < 30:
            print("The story is too short")
            return
        
        start_point = random.randint(0, GAMEPLAY_DURATION - audio_duration)
        end_point = start_point + audio_duration

        video = VideoFileClip(GAMEPLAY_FILE_PATH).subclip(start_point, end_point)
        audio = AudioFileClip(self.audio_file_path)

        video = video.set_audio(audio)
        video.write_videofile(self.video_file_path, codec='libx264', audio_codec='aac')

    def transcribe_video(self, model_size="medium"):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(device)
        model = whisper.load_model(model_size, device=device)
        audio = whisper.load_audio(self.video_file_path)
        result = whisper.transcribe(model=model, audio=audio, language="en")
        text_clips_array = []
        segments = result["segments"]
        # for segment in segments:
        #     condense_segment = condense_captions(segment=segment, threshold=9)
        #     for phrase in condense_segment.keys(): # each value is list [a, b], where a is start time and b is end time
        #         text_clip = TextClip(txt=phrase, fontsize=90, stroke_color="black", method="caption",
        #                              stroke_width=5, color="white", font=self.font_path, size=(570, None))
        #         text_clip = text_clip.set_start(condense_segment[phrase][0]).set_end(condense_segment[phrase][1]).set_position("center")
        #         text_clips_array.append(text_clip)   
        segments = result["segments"]
        for segment in segments:
            for word in segment["words"]:
                text_clip = TextClip(txt=word["text"], fontsize=90, stroke_color="black", size=(450, None),
                                     method="caption", stroke_width=5, color="white", font=self.font_path)
                text_clip = text_clip.set_start(word["start"]).set_end(word["end"]).set_position("center")
                text_clips_array.append(text_clip)   

        original_clip = VideoFileClip(self.video_file_path)

        final_video = CompositeVideoClip([original_clip] + text_clips_array)
        final_video.write_videofile(f"results/{self.post_id}.mp4", codec='libx264') 

    def add_background_music(self):
        bg_music_list = ["music/snowfall.mp3", "music/fallen_down.mp3"]
        random_index = random.randint(0, len(bg_music_list) - 1)
        background_music_path = bg_music_list[random_index]
        music_duration = librosa.get_duration(filename=background_music_path)
        audio_duration = librosa.get_duration(filename=self.audio_file_path)

        if audio_duration > 10 * 60: # no longer than 10 minutes
            print("Story too long")
            return

        while int(audio_duration) > int(music_duration):
            random_index = random.randint(0, len(bg_music_list) - 1)
            background_music_path = bg_music_list[random_index]          
        
        start = random.randint(0, int(music_duration - audio_duration) - 1)
        end = audio_duration + start

        video = VideoFileClip(f"results/{self.post_id}.mp4")
        
        audio_bg_subclip = AudioFileClip(background_music_path).subclip(start, end)
        audio_bg_subclip = audio_bg_subclip.volumex(0.14)

        final_audio = CompositeAudioClip([video.audio, audio_bg_subclip])
        
        final_video = video.set_audio(final_audio)
        final_video.write_videofile(self.video_file_path)

    def generate_intro_clip(self):
        image_header = Image.open("header.png")
        image_footer = Image.open("footer.png")
        header_w, header_h = image_header.size
        footer_w, footer_h = image_footer.size
        desired_clip_width = int(720*0.8)
        tc = TextClip(txt=self.post_title, fontsize=45, method="caption", color="black", kerning=-2,
              font="Arial-SemiBold", bg_color="white", size=(desired_clip_width, None))
        tc = tc.set_position("center").set_duration(1)
        frame = tc.get_frame(0)
        text_frame = Image.fromarray(frame)
        text_frame.save("text_frame.png")

        new_image = Image.new("RGB", (max(header_w, text_frame.width, footer_w) + 40, 
                                      header_h + text_frame.height + footer_h + 55), color="white")
        new_image.paste(image_header, (20, 15))
        new_image.paste(text_frame, (20, header_h + 15 + 10))
        new_image.paste(image_footer, (20, header_h + 15 + 10 + text_frame.height + 20))
        new_image.save(self.image_file_path)

        audio_title_duration = librosa.get_duration(filename="title.mp3")

        image_clip = ImageClip(img=self.image_file_path).set_duration(audio_title_duration)
        image_clip.write_videofile("intro_clip.mp4", fps=24)
    
    def overlay_intro_clip(self):
        main_video = VideoFileClip(self.video_file_path)
        intro_clip = VideoFileClip("intro_clip.mp4")
        composite_clip = CompositeVideoClip([main_video, intro_clip.set_position(('center', 'center'))])
        composite_clip.write_videofile(f"results/{self.post_id}.mp4")




        
    