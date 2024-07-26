import praw
from text_to_speech import createVoiceOver
from video_editor import createVideo
from dotenv import load_dotenv
import os

load_dotenv()

reddit = praw.Reddit(
    client_id=os.environ.get("CLIENT_ID"),
    client_secret=os.environ.get("CLIENT_SECRET"),
    password=os.environ.get("PASSWORD"),
    user_agent=os.environ.get("USER_AGENT"),
    username=os.environ.get("USERNAME"),
)

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
    def create_movie(self):
        if not self.audio_file_path or not self.video_file_path:
            return
        createVideo(self.audio_file_path, self.video_file_path)
    
        

name_of_subbreddit = "stories"
subreddits = list(reddit.subreddit(name_of_subbreddit).top(time_filter="day", limit=2))
subreddits = [subreddit for subreddit in subreddits if subreddit.over_18 == False] # dont include over 18 content

stories = [Story() for _ in range(len(subreddits))]
    
def getInformation():
    for i in range(len(subreddits)):
        stories[i].set_post_id(subreddits[i].id)
        stories[i].set_post_title(subreddits[i].title)
        stories[i].set_submission_self_text(subreddits[i].selftext)
        stories[i].set_post_url(subreddits[i].url)
        author = "NONETYPE" if subreddits[i].author is None else subreddits[i].author.name
        stories[i].set_post_author(author)

def createVoiceOverForAllStories():
    for s in stories:
        s.create_voiceover()

def createMoviesForAllStories():
    for s in stories:
        s.create_movie()


getInformation()
createVoiceOverForAllStories()