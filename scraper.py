import praw # library for interacting with the Reddit API
import requests # library for sending HTTP requests
import random # library for generating random numbers
import concurrent.futures # library for running multiple threads in parallel

# create a Reddit object with client_id, client_secret, and user_agent
reddit = praw.Reddit(
    client_id="", # Your client ID goes here
    client_secret="", # Your client secret goes here
    user_agent="", # Your user agent goes here
)

# minimum number of upvotes for a post to be considered valid
likeCount = 700
 
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
                        titleauthor = (submission.title + submission.author.name).lower().replace(" ", "") + "\n"
                        titleauthor_bytes = titleauthor.encode('utf-8')
                        with open("posts.txt", "a+") as f:
                            data = f.read()
                            # check if the post title & author name already exists in the text file
                            if data.find(titleauthor) == -1:
                                f.write(titleauthor)
                                # Download the image
                                response = requests.get(direct_image_url)
                                with open("images/" + submission.title + ".jpeg", "wb") as f:
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

# use ThreadPoolExecutor to run scanReddit function for each subreddit in parallel
with concurrent.futures.ThreadPoolExecutor() as executor:
    for subreddit in subreddit_list:
        executor.submit(scanReddit, subreddit)
