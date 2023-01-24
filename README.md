# trippin.online   

This is a project I made for fun.

# Script descriptions:
- scrape.py:
This is the main image scraper, this will go through the list of subreddits in the code and download images with more than 700 upvotes, it will then download the image and store it in the images folder.
This script is currently running 24/7 so will always generate new images.
 
- index.php:
This is what the frontend uses, this will grab a random .jpeg from the images folder and show it to the user for 3 minutes unless the t variable is used in the url, in which case it will show for that amount of seconds before refreshing for a new image.
There is cookie storage to store which images the user has already been shown so their is no duplicates.

# Contact
For any enquiries related to this project please email contact (at) trippin (dot) online
