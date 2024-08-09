## This code is all ChatGPT generated, but the script is much better now. See release notes (generated by ChatGPT lol)

import os
import praw
import requests
import random
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
from hashlib import sha1
from PIL import Image
from io import BytesIO

# Global variables for rate limiting
QUERY_LIMIT = 100  # Maximum queries per minute
QUERY_INTERVAL = 60  # Time interval in seconds for rate limiting
query_counter = 0

# Check if the posts.json file exists, if not create it
if not os.path.exists("posts.json"):
    with open("posts.json", "w") as f:
        json.dump({}, f)

# Replace with your actual Reddit API credentials
reddit = praw.Reddit(
    client_id="",  # Your client ID goes here
    client_secret="",  # Your client secret goes here
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
)

like_count = 800
image_count = 100

data = {}

def rate_limit():
    global query_counter
    query_counter += 1
    if query_counter > QUERY_LIMIT:
        time.sleep(QUERY_INTERVAL)
        query_counter = 0

def save_image_as_webp(image_url, file_name, subreddit_name):
    rate_limit()  # Enforce rate limit
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    webp_file_name = f"{file_name}.webp"
    image.save(webp_file_name, "webp")
    print(f"{subreddit_name}: Saved image as {webp_file_name}")

def scan_reddit(subreddit_name):
    """
    Scans subreddit for valid image posts.
    """
    try:
        print(f"Starting to search for valid posts on r/{subreddit_name}")
        i = 0
        while i < image_count:
            rate_limit()  # Enforce rate limit
            subreddit = reddit.subreddit(subreddit_name)
            submissions = list(subreddit.hot(limit=250))  # Limit the number of submissions to consider
            submission = random.choice(submissions)
            if not submission.is_self and submission.score > like_count:
                images = submission.preview.get("images")
                if images:
                    print(f"\n{subreddit_name}: Image found with {submission.score} upvotes")
                    for image in images:
                        direct_image_url = image["source"]["url"]
                        title_author = sha1((submission.title + submission.author.name).encode('utf-8')).hexdigest()
                        if title_author not in data:
                            data[title_author] = direct_image_url
                            with open("posts.json", "w") as f:
                                json.dump(data, f)
                            safe_title = "".join(x for x in submission.title if x.isalnum() or x in "._- ")
                            file_name = f"images/{safe_title}"
                            if not os.path.exists(f"{file_name}.webp"):
                                save_image_as_webp(direct_image_url, file_name, subreddit_name)
                                i += 1
                            else:
                                print(f"{subreddit_name}: File already exists for {safe_title}. Skipping download.")
                        else:
                            print(f"{subreddit_name}: Post data already exists.")
                else:
                    print(f"{subreddit_name}: Post is not an image post.")
            else:
                if submission.is_self:
                    print(f"{subreddit_name}: Skipping text post.")
                else:
                    print(f"{subreddit_name}: Skipping post with {submission.score}/{like_count} upvotes.")
            if i >= image_count:
                print(f"{subreddit_name}: 100 images downloaded. Sleeping for 24 hours.")
                time.sleep(86400)
                i = 0
    except Exception as e:
        print(f"{subreddit_name} generated an exception: {e}")

# List of subreddits to scan
subreddit_list = ["EarthPorn", "SkyPorn", "ArtPorn", "ExposurePorn"]

while True:
    try:
        with ProcessPoolExecutor(max_workers=4) as executor:
            future_to_subreddit = {executor.submit(scan_reddit, subreddit): subreddit for subreddit in subreddit_list}
            for future in as_completed(future_to_subreddit):
                subreddit = future_to_subreddit[future]
                try:
                    data = future.result()
                except Exception as exc:
                    print(f'{subreddit} generated an exception: {exc}')
                else:
                    print(f'{subreddit} page processed.')
    except Exception as e:
        print(f"Main process encountered an exception: {e}")
        time.sleep(60)  # Wait for 60 seconds before retrying
