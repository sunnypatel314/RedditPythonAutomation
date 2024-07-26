from moviepy.editor import *
import librosa
import random

def createVideo(audio_file_path, video_output_path):
    GAMEPLAY_FILE_PATH = "background/mc2.mp4"
    GAMEPLAY_DURATION = int(VideoFileClip(GAMEPLAY_FILE_PATH).duration)

    audio_duration = int(librosa.get_duration(path=audio_file_path)) + 1

    if audio_duration > GAMEPLAY_DURATION or audio_duration == 0:
        return
    start_point = random.randint(0, GAMEPLAY_DURATION - audio_duration)
    end_point = start_point + audio_duration

    video = VideoFileClip(GAMEPLAY_FILE_PATH).subclip(start_point, end_point)
    audio = AudioFileClip(audio_file_path)

    video = video.set_audio(audio)
    video.write_videofile(video_output_path, codec='libx264', audio_codec='aac')


    



    
