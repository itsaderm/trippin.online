# trippin.online   
The idea for this project is to give people who enjoy tripping on psychedelics nice images to look at and trip balls to.. for 3 minutes before it refreshes and shows you a new image to use all your brain cells on. 

This is for pure fun of messing around with Python, PHP and OpenAI as all of the code here was generated by OpenAI. I have little Python/PHP knowledge so don't waste time with pull requests etc.

You can view the website live [here](https://trippin.online)

# Script descriptions:
- scraper.py:
This is the main image scraper, this will go through the list of subreddits in the code and download images with more than 700 upvotes, it will then download the image and store it in the images folder.
This script is currently running 24/7 so will always generate new images.
 
- index.php:
This is what the frontend uses, this will grab a random .jpeg from the images folder and show it to the user for 3 minutes unless the t variable is used in the url, in which case it will show for that amount of seconds before refreshing for a new image.
There is cookie storage to store which images the user has already been shown so their is no duplicates.

# Contact
For any enquiries related to this project please email contact (at) trippin (dot) online
