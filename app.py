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

name_of_subbreddit, word_count_limit = "stories", 3500
subreddits = list(reddit.subreddit(name_of_subbreddit).top(time_filter="day", limit=2))
subreddits = [subreddit for subreddit in subreddits if not subreddit.over_18 # don't include over 18 content
              and len(subreddit.selftext) <= word_count_limit] 

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
        stories[i].set_font_path("fonts/Roboto-Bold.ttf")
        print(subreddits[i].title)
        print(subreddits[i].url)

s = Story()
s.post_title = "Beneath the ancient oak, a small rabbit hopped, searching for the elusive golden leaf. The sky turned crimson as twilight approached."
s.submission_self_text = "In the midst of a bustling city, a hidden garden thrived with vibrant flowers and chirping birds. Each morning, the sun's rays danced through the leaves, casting playful shadows on the cobblestone paths. Visitors, enchanted by the serene beauty, often paused to capture the moment, leaving with hearts lighter and spirits uplifted."
s.set_post_id("31415")
s.set_font_path("fonts/Roboto-Bold.ttf")

stories = [s]

def create_reddit_stories():
    for s in stories:
        if doesPostExist(s.post_id):
            continue
        try:
            start = time.time()
            s.create_voiceover()
            print("created voiceover ", s.post_id)
            s.create_video()
            print("created video ", s.post_id) 
            s.transcribe_video()
            print("transcribed video ", s.post_id) 
            s.add_background_music() 
            print("added bg music ", s.post_id)
            s.generate_intro_clip()
            print("generated intro clip ", s.post_id) 
            s.overlay_intro_clip()
            print("overlayed intro clip ", s.post_id) 
            end = time.time()
            print(end - start, len(s.submission_self_text))
        except Exception as e:
            print(e)
        

# get_information()
create_reddit_stories()


directories_to_remove = ["audio", "videos"] # can also add "images" but i decide to keep them
files_to_remove = ["intro_clip.mp4", "text_frame.png", "title.mp3", "body.mp3"]
removeUnwantedContent(directories=directories_to_remove, files=files_to_remove)
