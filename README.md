# trippin.online

## Overview
trippin.online is a web application designed to offer a visually captivating experience. Combining Python and PHP, the site presents a curated collection of images that refresh every few minutes, creating an engaging and immersive visual environment.

## Live Demo
View the live site on [adaml.vip](https://adaml.vip) - I no longer have have the original domain, it is instead stored on my personal site.

## Components

### **Image Scraper (scraper.py)**
- Scrapes high-upvote images from the configurable subreddits: EarthPorn, SkyPorn, ExposurePorn and ArtPorn.
- Saves images in the `images` folder and runs continuously to keep the collection fresh.

### **Image Display Frontend (index.php)**
- Randomly selects and displays an image from the `images` folder.
- Refreshes every 5 minutes by default, or as specified by the `/?t=` parameter in the URL.
- Uses session management to avoid showing duplicate images within a session.

## Technical Details
- **Rate Limiting:** Implemented in `scraper.py` with a limit of 100 requests per 60 seconds.
- **Cache Control:** Disables caching to always present the latest content.

## Note
This project is designed to provide an engaging and enjoyable visual experience, making it a perfect choice for those seeking a relaxing and immersive environment.

## Contact
For inquiries, contact me on Discord: `aderm.`
