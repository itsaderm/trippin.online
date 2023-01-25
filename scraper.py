import os
import praw # library for interacting with the Reddit API
import requests # library for sending HTTP requests
import random # library for generating random numbers
from concurrent.futures import ProcessPoolExecutor # library for running multiple threads in parallel
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
likeCount = 700

# Create a dictionary to store post title & author name as key and direct_image_url as value
data = {}

def scanReddit(name):
    """
    Scans subreddit for valid image posts.
    """
    found_valid_post = False
    print("Starting to search for valid post on r/", name)
    while True:
        # Get direct image URLs from subreddit
        subreddit = reddit.subreddit(name)
        submissions = subreddit.hot() # retrieve the 'hot' posts from the subreddit
        submissions = list(submissions) # convert the generator to a list
        submission = random.choice(submissions) # select a random submission from the list
        if not submission.is_self:
            if submission.score > likeCount:
                images = submission.preview.get("images")
                if images:
                    found_valid_post = True
                    print("Image found with " + str(submission.score) + " upvotes.. Downloading: \n" + submission.title)
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
                        else:
                            print("Post data already exists.")
                else:
                    print("Post is not an image post.")
            else:
                print("Image found but " + str(submission.score) + "/700 upvotes needed.. Continuing search")
        else:
            print("Post is a text post.")

# list of subreddit names to scan 
subreddit_list = ["EarthPorn", "SpacePorn", "SkyPorn", "Art", "ExposurePorn"]

# create an instance of the ProcessPoolExecutor with max_workers = 4
with ProcessPoolExecutor(max_workers=4) as executor:
    # for each subreddit in subreddit_list
    for subreddit in subreddit_list:
        # submit the scanReddit function with the subreddit to the executor
        executor.submit(scanReddit, subreddit)

# the script will continue running indefinitely
while True:
    continue
