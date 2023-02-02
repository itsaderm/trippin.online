import os
import praw # library for interacting with the Reddit API
import requests # library for sending HTTP requests
import random # library for generating random numbers
import time # library for sleep
from concurrent.futures import ProcessPoolExecutor # library for running multiple threads in parallel
from concurrent.futures import as_completed
import json # library for working with JSON data

# Check if the posts.json file exists, if not create it
if not os.path.exists("posts.json"):
    with open("posts.json", "w") as f:
        json.dump({}, f)

# create a Reddit object with client_id, client_secret, and user_agent
reddit = praw.Reddit(
    client_id="", # Your client ID goes here
    client_secret="", # Your client secret goes here
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36", # Your user agent goes here
)
# minimum number of upvotes for a post to be considered valid
likeCount = 500

# amount of images to download before sleeping 
imageCount = 100

# Create a dictionary to store post title & author name as key and direct_image_url as value
data = {}

def scanReddit(name):
    """
    Scans subreddit for valid image posts.
    """
    print(f"Starting to search for valid post on r/{name}")
    i = 0
    while i < imageCount:
        # Get direct image URLs from subreddit
        subreddit = reddit.subreddit(name)
        submissions = subreddit.hot() # retrieve the 'hot' posts from the subreddit
        submissions = list(submissions) # convert the generator to a list
        submission = random.choice(submissions) # select a random submission from the list
        if not submission.is_self:
            if submission.score > likeCount:
                images = submission.preview.get("images")
                if images:
                    print(f"\nImage found with {submission.score} upvotes")
                    for image in images:
                        direct_image_url = image["source"]["url"]
                        # Create a string of the post title & author name.
                        titleauthor = (submission.title + submission.author.name).lower().replace(" ", "")
                        # Check if the post title & author name already exists in the data dictionary
                        if titleauthor not in data:
                            data[titleauthor] = direct_image_url
                            # dump data to the file
                            with open("posts.json", "w") as f:
                                json.dump(data, f)
                            # Download the image
                            response = requests.get(direct_image_url)
                            with open("images/" + submission.title + ".webp", "wb") as f:
                                f.write(response.content)
                            print(f"r/{subreddit} - {submission.title} - Downloaded")
                        else:
                            print("Post data already exists.")
                        i = i+1
                else:
                    print("Post is not an image post.")
            else:
                print(f"Image found but {submission.score}/{likeCount} upvotes needed.. Continuing search")
        else:
            print("Post is a text post.")
        if i == 100:
            print("100 images downloaded. Sleeping for 24 hours.")
            time.sleep(86400)
            i = 0



# list of subreddit names to scan 
subreddit_list = ["EarthPorn", "SpacePorn", "SkyPorn", "Art", "ExposurePorn"]

with ProcessPoolExecutor(max_workers=4) as executor:
    # submit the scanReddit function with the subreddit to the executor
    future_to_subreddit = {executor.submit(scanReddit, subreddit): subreddit for subreddit in subreddit_list}
    for future in as_completed(future_to_subreddit):
        subreddit = future_to_subreddit[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (subreddit, exc))
        else:
            print('%r page is %d bytes' % (subreddit, len(data)))
