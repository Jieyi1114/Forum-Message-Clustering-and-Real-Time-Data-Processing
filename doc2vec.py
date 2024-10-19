from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
import numpy as np

# Train and apply Doc2Vec model directly inside get_doc2vec_df
def get_doc2vec_df(df):
    if not df.empty:
        # Pre-process posts to create TaggedDocuments for training
        # Replace NaN values with empty strings
        df = df.dropna(subset=['selftext'])
        posts = df['selftext']
        tagged_data = [TaggedDocument(words=post.split(), tags=[str(i)]) for i, post in enumerate(posts) if post]

        # Initialize and train the Doc2Vec model
        model = Doc2Vec(vector_size=50, alpha=0.025, min_alpha=0.00025, min_count=1, dm=1)
        model.build_vocab(tagged_data)
        for epoch in range(15):
            model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)
            model.alpha -= 0.002  # Decrease the learning rate
            model.min_alpha = model.alpha  # Fix the learning rate

        # Infer vectors for each selftext in the DataFrame
        vectors = posts.apply(lambda text: model.infer_vector(text.split()) if text else np.zeros(model.vector_size))

        # Add the vectors to the DataFrame
        df['selftext_vector'] = vectors.apply(lambda vec: ','.join(map(str, vec.tolist())))  # Convert to comma-separated string

        file_path = "./Cleaned_data_with_doc2vec.csv"
        df.to_csv(file_path, index=False)  # Save raw data to CSV
        print(f"Save clean data with doc2vec to {file_path} successfully!")

    return df, model