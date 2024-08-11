## This code is all ChatGPT generated, but the script is much better now. 
 
import os
import praw
import requests
import random
import time
import json
from PIL import Image
from io import BytesIO

# Global variables for rate limiting
QUERY_LIMIT = 100  # Maximum queries per minute
QUERY_INTERVAL = 60  # Time interval in seconds for rate limiting
query_counter = 0

# Maximum image size in pixels (width * height)
MAX_IMAGE_SIZE = 89478485  # Adjust this if needed

# Set the maximum image size limit for Pillow
Image.MAX_IMAGE_SIZE = MAX_IMAGE_SIZE

# Load or initialize the data store
if os.path.exists("processed_submissions.json"):
    with open("processed_submissions.json", "r") as f:
        processed_submissions = json.load(f)
else:
    processed_submissions = {}

# Replace with your actual Reddit API credentials
reddit = praw.Reddit(
    client_id="",  # Your client ID goes here
    client_secret="",  # Your client secret goes here
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
)

like_count = 750

def rate_limit():
    global query_counter
    query_counter += 1
    if query_counter >= QUERY_LIMIT:
        print("Rate limit reached. Sleeping for 60 seconds...")
        time.sleep(QUERY_INTERVAL)
        query_counter = 0

def save_image_as_webp(image_url, file_name, subreddit_name):
    rate_limit()  # Enforce rate limit
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Check for HTTP errors
        image = Image.open(BytesIO(response.content))
        
        # Check if image size exceeds the limit
        if image.width * image.height > MAX_IMAGE_SIZE:
            print(f"{subreddit_name}: Image is too large ({image.width * image.height} pixels). Skipping.")
            return False
        
        webp_file_name = f"images/{file_name}.webp"
        os.makedirs(os.path.dirname(webp_file_name), exist_ok=True)  # Ensure directory exists
        image.save(webp_file_name, "webp")
        print(f"{subreddit_name}: Saved image as {file_name}.webp")
        return True  # Indicate success
    except Exception as e:
        print(f"Error saving image {file_name}: {e}")
        return False  # Indicate failure

def scan_reddit(subreddit_name):
    """
    Scans a subreddit for a valid image post and saves it.
    """
    try:
        print(f"\nSearching for valid posts on r/{subreddit_name}")
        rate_limit()  # Enforce rate limit
        subreddit = reddit.subreddit(subreddit_name)
        submissions = list(subreddit.top())  # Get the list of top submissions
        random.shuffle(submissions)  # Shuffle to avoid any bias
        for submission in submissions:
            submission_id = submission.id

            # Initialize the list for the subreddit if it doesn't exist
            if subreddit_name not in processed_submissions:
                processed_submissions[subreddit_name] = []

            if submission_id not in processed_submissions[subreddit_name]:
                if not submission.is_self and submission.score > like_count:
                    images = submission.preview.get("images")
                    if images:
                        print(f"{subreddit_name}: Image found with {submission.score} upvotes")
                        for image in images:
                            direct_image_url = image["source"]["url"]
                            safe_title = "".join(x for x in submission.title if x.isalnum() or x in "._- ")
                            file_name = f"{safe_title}"
                            if not os.path.exists(f"images/{file_name}.webp"):
                                if save_image_as_webp(direct_image_url, file_name, subreddit_name):
                                    # Add the submission ID to the list and save the JSON file
                                    processed_submissions[subreddit_name].append(submission_id)
                                    with open("processed_submissions.json", "w") as f:
                                        json.dump(processed_submissions, f)
                                    return  # Exit after saving the image
                                else:
                                    print(f"{subreddit_name}: Failed to save image. Skipping post.")
                                    return  # Exit if saving the image failed
                            else:
                                print(f"{subreddit_name}: File already exists for {safe_title}. Skipping download.")
                    else:
                        print(f"{subreddit_name}: Post is not an image post.")
                else:
                    if submission.is_self:
                        print(f"{subreddit_name}: Skipping text post.")
                    else:
                        print(f"{subreddit_name}: Skipping post with {submission.score}/{like_count} upvotes.")
    except Exception as e:
        print(f"{subreddit_name} generated an exception: {e}")

# List of subreddits to scan
subreddit_list = ["EarthPorn", "SkyPorn", "ArtPorn", "ExposurePorn"]

while True:
    try:
        for subreddit in subreddit_list:
            scan_reddit(subreddit)
            # Sleep between subreddits to avoid hitting rate limits or causing API issues
            time.sleep(5)
    except Exception as e:
        print(f"Main process encountered an exception: {e}")
        time.sleep(60)  # Wait for 60 seconds before retrying
