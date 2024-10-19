import pandas as pd
import re
import warnings
from urllib.parse import urlparse
warnings.filterwarnings("ignore")

# In[38]:


class CleanUp:
    
    def __init__(self, stop_words, file_path):
        self.stop_words = stop_words
        self.file_path = file_path
        
    def clean_text(self, text):
        # Remove punctuation
        text = re.sub(r'[^\w\s]', '', text)
        # Convert to lowercase
        text = text.lower()
        # Remove extra spaces
        text = " ".join(text.split())
        # Remove stopwords
        text = " ".join([word for word in text.split() if word not in self.stop_words])
        # Remove digits
        text = re.sub(r'\d+', '', text)
        return text

    def extract_last_part(self, url):
        # Parse the URL
        parsed_url = urlparse(url)
        # Get the path part of the URL and split it by '/'
        path = parsed_url.path.split('/')
        # Get the last non-empty part (slug) from the URL
        path_clean = path[-1] if path[-1] else path[-2]
        # Return the slug with hyphens replaced by spaces
        return str(path_clean).replace('-', ' ')
    
    def apply_clean_to_dataframe(self):
        # Load the CSV file into a DataFrame
        reddit_data = pd.read_csv(self.file_path)
        
        # Convert the 'created_utc' to yyyymmdd format
        reddit_data['time_stamp'] = pd.to_datetime(reddit_data['created_utc']).dt.strftime('%Y%m%d')
        reddit_data['title'] = reddit_data['title'].apply(self.clean_text)
        #reddit_data['extracted_text'] = reddit_data['extracted_text'].astype(str).apply(self.clean_text)
        reddit_data['url'] = reddit_data['url'].apply(self.extract_last_part)
        reddit_data['url'] = reddit_data['url'].apply(self.clean_text)
        reddit_data = reddit_data.drop(['created_utc'], axis=1, errors='ignore')
        #print(reddit_data.columns)
        return reddit_data




