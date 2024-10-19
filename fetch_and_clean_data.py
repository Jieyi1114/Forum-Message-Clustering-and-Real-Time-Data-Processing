import praw
import pandas as pd
from datetime import datetime
from praw_config import initialize_reddit
import requests
from PIL import Image, ImageOps
import pytesseract
import io
import os
from nltk.corpus import stopwords
import nltk
from TextCleanUp import CleanUp
import warnings
from urllib.parse import urlparse

warnings.filterwarnings("ignore")

image_folder = './images'

# Initialize nltk
nltk.download('stopwords')

def fetch_image_from_url(url):
    response = requests.get(url)
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    return Image.open(io.BytesIO(response.content))

def extract_text_from_image(image):
    custom_config = r'--oem 3 --psm 11'
    gray_image = ImageOps.grayscale(image)
    text = pytesseract.image_to_string(gray_image, config=custom_config)
    cleaned_text = ' '.join(text.split()).strip()
    return cleaned_text

def get_image_url(submission):
    """Get image URL from the submission if available."""
    if hasattr(submission, 'preview'):
        images = submission.preview.get('images')
        if images:
            return images[0]['source']['url']  # Get the highest resolution image


def fetch_data(num_posts, subreddit='USC'):
    """Fetch a specified number of posts from a given subreddit."""
    reddit = initialize_reddit()
    posts = []
    try:
        for submission in reddit.subreddit(subreddit).new(limit=num_posts):
            post_data = {
                "id": submission.id,
                "title": submission.title,
                "score": submission.score,
                "url": submission.url,
                "num_comments": submission.num_comments,
                "selftext": submission.selftext if submission.is_self else None,
                "created_utc": datetime.fromtimestamp(submission.created_utc)
            }

            #image_url = get_image_url(submission)

            # If there's an image URL, fetch the image and extract text
            #if image_url:
            #     image = fetch_image_from_url(image_url)
            #     print(image)
            #     if image:
            #         extracted_text = extract_text_from_image(image)
            #         post_data["extracted_text"] = extracted_text
            #     else:
            #         post_data["extracted_text"] = "Failed to fetch the image"
            # else:
            #     post_data["extracted_text"] = None

            posts.append(post_data)
    except Exception as e:
        print(f"An error occurred: {e}")

    # Create DataFrame
    df = pd.DataFrame(posts)
    return df


def clean_data(df):
    """Clean the fetched data."""
    stop_words = set(stopwords.words('english'))
    file_path = "./Praw_Data.csv"
    df.to_csv(file_path, index=False)  # Save raw data to CSV
    print(f"Save raw data to {file_path} successfully!")

    # Initialize cleanup class
    Clean_Up = CleanUp(stop_words, file_path)
    clean_df = Clean_Up.apply_clean_to_dataframe()
    
    # Save cleaned data to CSV
    cleaned_file_path = "./Cleaned_Praw_Data.csv"
    clean_df.to_csv(cleaned_file_path, index=False)
    print(f"Save clean data to {cleaned_file_path} successfully!")

    # Return the cleaned DataFrame
    return clean_df