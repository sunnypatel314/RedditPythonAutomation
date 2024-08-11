import time
import praw
import os
from classes.Story import Story
from utils.check_post_id import doesPostExist
from utils.clean_text import cleanText, containsMultipleParts
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
char_count_min, char_count_max = 700, 3500
posts = list(reddit.subreddit(name_of_subbreddit).top(time_filter="day", limit=10))
print([len(p.selftext) for p in posts])
print([p.title for p in posts])
posts = [p for p in posts if not containsMultipleParts(p.title.strip()) 
         and len(p.selftext) >= char_count_min # make sure length is within range
         and len(p.selftext) <= char_count_max]                  

if not posts:
    print("No posts fit the requirements.")

stories = [Story() for _ in range(len(posts))]

directories_to_create = ["audio", "videos", "images", "results"]
makeDirectories(directories=directories_to_create)

def get_information():
    for i in range(len(posts)):
        stories[i].set_post_id(posts[i].id)
        stories[i].set_post_title(posts[i].title)
        cleaned_submission_self_text = cleanText(posts[i].selftext)
        stories[i].set_submission_self_text(cleaned_submission_self_text)
        stories[i].set_post_url(posts[i].url)
        author = "NONETYPE" if posts[i].author is None else posts[i].author.name
        stories[i].set_post_author(author)
        stories[i].set_font_path("fonts/Poppins-Bold.ttf")
        print(posts[i].title, len(posts[i].selftext))
        print(posts[i].url)

# s = Story()
# s.post_title = "Beneath the ancient oak, a small rabbit hopped, searching for the elusive golden leaf. The sky turned crimson as twilight approached."
# s.submission_self_text = "often paused to capture the moment, leaving with hearts lighter and spirits uplifted."
# s.set_post_id("31415")
# s.set_font_path("fonts/Roboto-Bold.ttf")
# stories = [s]

def create_reddit_stories():
    for s in stories:
        if doesPostExist(s.post_id):
            print(f"Post #{s.post_id} has already been made")
            continue
        try:
            start = time.time()
            s.create_voiceover()
            s.generate_intro_clip()
            initial_vid = s.create_video()
            transcribed_vid = s.transcribe_video(initial_vid)
            vid_with_bg_music = s.add_background_music(transcribed_vid) 
            s.overlay_intro_clip(vid_with_bg_music)
            end = time.time()
            print(end - start, len(s.submission_self_text))
            # s.send_video_via_email(recipient_email="sunnypatel4prez@gmail.com")
        except Exception as e:
            print(e)
        # break
        

get_information()
create_reddit_stories()


directories_to_remove = ["audio", "videos"] # can also add "images" but i decide to keep them
files_to_remove = ["intro_clip.mp4", "text_frame.png", "title.mp3", "body.mp3"]
removeUnwantedContent(directories=directories_to_remove, files=files_to_remove)
