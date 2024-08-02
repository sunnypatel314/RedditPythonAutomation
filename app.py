import time
import praw
import os
from classes.Story import Story
from utils.check_post_id import doesPostExist
from utils.clean_text import cleanText
from utils.directories import makeDirectories, removeUnwantedContent
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.environ.get("CLIENT_ID"),
    client_secret=os.environ.get("CLIENT_SECRET"),
    password=os.environ.get("PASSWORD"),
    user_agent=os.environ.get("USER_AGENT"),
    username=os.environ.get("USERNAME"),
)           

name_of_subbreddit = "stories"
subreddits = list(reddit.subreddit(name_of_subbreddit).top(time_filter="day", limit=3))
subreddits = [subreddit for subreddit in subreddits if not subreddit.over_18 and len(subreddit.selftext) < 5000] # don't include over 18 content

stories = [Story() for _ in range(len(subreddits))]

directories_to_create = ["audio", "videos", "images", "results"]
makeDirectories(directories=directories_to_create)

def get_information():
    for i in range(len(subreddits)):
        stories[i].set_post_id(subreddits[i].id)
        stories[i].set_post_title(subreddits[i].title)
        cleaned_submission_self_text = cleanText(subreddits[i].selftext)
        stories[i].set_submission_self_text(cleaned_submission_self_text)
        stories[i].set_post_url(subreddits[i].url)
        author = "NONETYPE" if subreddits[i].author is None else subreddits[i].author.name
        stories[i].set_post_author(author)
        stories[i].set_font_path("fonts/Roboto-BlackItalic.ttf")
        print(subreddits[i].title)
        print(subreddits[i].url)

def create_reddit_stories():
    for s in stories:
        if doesPostExist(s.post_id):
            continue
        try:
            start = time.time()
            s.create_voiceover()
            s.create_video()
            s.transcribe_video()
            s.add_background_music()
            s.generate_intro_clip()
            s.overlay_intro_clip()
            end = time.time()
            print(end - start, len(s.submission_self_text))
        except Exception as e:
            print(e)




get_information()
create_reddit_stories()


directories_to_remove = ["audio", "videos"] # can also add "images" but i decide to keep them
files_to_remove = ["intro_clip.mp4", "text_frame.png", "title.mp3", "body.mp3"]
removeUnwantedContent(directories=directories_to_remove, files=files_to_remove)
