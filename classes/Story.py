from utils.text_to_speech import createVoiceOver
from utils.video_editor import createVideo

class Story():
    def __init__(self) -> None:
        self.post_title = ""
        self.submission_self_text = ""
        self.post_url = ""
        self.post_id = ""
        self.post_author = ""
        self.audio_file_path = ""
        self.video_file_path = ""
    def set_post_id(self, id):
        self.post_id = id
        self.audio_file_path = f"audio/post-{id}.wav"
        self.video_file_path = f"video/post-{id}.mp4"
    def set_post_title(self, title):
        self.post_title = title
    def set_post_author(self, author):
        self.post_author = author
    def set_submission_self_text(self, text):
        self.submission_self_text = text
    def set_post_url(self, post_url):
        self.post_url = post_url
    def create_voiceover(self):
        if not self.audio_file_path or not self.submission_self_text:
            return
        createVoiceOver(self.submission_self_text, self.audio_file_path)
    def create_video(self):
        if not self.audio_file_path or not self.video_file_path:
            return
        createVideo(self.audio_file_path, self.video_file_path)