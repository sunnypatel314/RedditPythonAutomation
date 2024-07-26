import re

def cleanText(text):
    # Define a regular expression pattern to match Markdown links
    markdown_link_pattern = r'\[.*?\]\(https?://[^\)]+\)'
    
    # Define a regular expression pattern to match HTML tags
    html_tag_pattern = r'<[^>]*>'
    
    # Define a regular expression pattern to match emojis (Unicode ranges for common emojis)
    emoji_pattern = r'[\U0001F600-\U0001F64F]|\U0001F300-\U0001F5FF|\U0001F680-\U0001F6FF|\U0001F700-\U0001F77F|\U0001F780-\U0001F7FF|\U0001F800-\U0001F8FF|\U0001F900-\U0001F9FF|\U0001FA00-\U0001FA6F|\U0001FA70-\U0001FAFF|\U00002700-\U000027BF|\U000024C2-\U000024C2'

    # Remove Markdown links
    text = re.sub(markdown_link_pattern, '', text)
    
    # Remove HTML tags
    text = re.sub(html_tag_pattern, '', text)
    
    # Remove emojis
    text = re.sub(emoji_pattern, '', text)
    
    # Remove any leading/trailing whitespace and excess whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text.strip()


