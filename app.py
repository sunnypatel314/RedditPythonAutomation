import praw
import os
from classes.Story import Story
from utils.clean_text import cleanText

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
subreddits = list(reddit.subreddit(name_of_subbreddit).top(time_filter="day", limit=2))
subreddits = [subreddit for subreddit in subreddits if subreddit.over_18 == False] # dont include over 18 content

stories = [Story() for _ in range(len(subreddits))]
    
def getInformation():
    for i in range(len(subreddits)):
        stories[i].set_post_id(subreddits[i].id)
        stories[i].set_post_title(subreddits[i].title)
        cleaned_submission_self_text = cleanText(subreddits[i].selftext)
        stories[i].set_submission_self_text(cleaned_submission_self_text)
        stories[i].set_post_url(subreddits[i].url)
        author = "NONETYPE" if subreddits[i].author is None else subreddits[i].author.name
        stories[i].set_post_author(author)

def createVoiceOverForAllStories():
    for s in stories:
        s.create_voiceover()

def createMoviesForAllStories():
    for s in stories:
        s.create_video()

getInformation()
createVoiceOverForAllStories()
createMoviesForAllStories()
