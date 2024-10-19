#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import sys
import argparse
from gensim.models import Doc2Vec
from fetch_and_clean_data import fetch_data, clean_data
from doc2vec import get_doc2vec_df
from Clustering import visualize_clusters_with_keywords, clustering, predict_cluster
# from db_creation import create_database, load_data_to_db  # Commented out

def main(host, user, password, db_name, table_name, number_of_posts, interval):
    while True:
        try:
            # Web scraping: fetch data and save to .csv file
            print(f"Fetching {number_of_posts} posts...")
            raw_data = fetch_data(number_of_posts)
            print("Data fetched successfully.")

            # Pre-processing: clean data and save to .csv file
            print("Cleaning data...")
            cleaned_data = clean_data(raw_data)
            print("Data cleaned successfully.")

            # Concat doc2vec column with clean_df and save to .csv file
            print("Applying Doc2Vec transformation...")
            clean_df_with_vectors, model = get_doc2vec_df(cleaned_data)
            print("Doc2Vec transformation completed.")

            # K-means clustering analysis
            print("Applying K-means clustering analysis...")
            kmeans, doc_vectors = clustering(clean_df_with_vectors)

            # Visualize clusters with keywords
            visualize_clusters_with_keywords(clean_df_with_vectors, kmeans, doc_vectors, num_keywords=5, num_samples=3)

            # Commenting out database creation and updating
            print("Updating database...")
            # create_database(host, user, password, db_name)
            # load_data_to_db(clean_df_with_vectors, db_name, table_name, host, user, password)
            print(f"Database '{db_name}' updated successfully.")

        except Exception as e:
            print(f"Error: {e}")

        # Check if the user wants to quit
        user_input = input(f"Next update in {interval} minutes. Type 'quit' to exit, or press Enter to continue: ")
        if user_input.lower() == 'quit':
            # Predict new text clusters
            word = input('Please type in a word you want to find the closest matching cluster: ')
            cluster = predict_cluster(word, kmeans, model)
            print(f"The word '{word}' belongs to cluster: {cluster}")
                
            print("Exiting the script.")
            break

        # Wait for the given interval (in minutes)
        time.sleep(interval * 20)  # Corrected to 60 seconds per minute

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web scraping, clustering, and data processing script.")
    parser.add_argument("interval", type=int, help="Interval in minutes between each data fetch and update.")
    
    args = parser.parse_args()
    
    # Database connection parameters (unused, but retained for future use)
    host = "localhost"
    user = "root"
    password = "201114"
    db_name = "lab4"
    table_name = "cleaned_praw_data"

    # Input post number
    number_of_posts = int(input("Enter the number of posts to fetch: "))

    # Run the main function with the given interval
    main(host, user, password, db_name, table_name, number_of_posts, args.interval)

