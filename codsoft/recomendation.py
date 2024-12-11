#collaborative filtering
import pandas as pd
from surprise import Dataset, Reader
from surprise import SVD, accuracy
from surprise.model_selection import train_test_split

# Sample dataset of users and movie ratings
data = {
    'user_id': ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'E', 'E'],
    'item_id': ['Movie1', 'Movie2', 'Movie3', 'Movie4', 'Movie1', 'Movie5', 'Movie2', 'Movie3', 'Movie4', 'Movie5'],
    'rating': [5, 4, 4, 5, 5, 3, 4, 2, 5, 4]
}

# Convert the dictionary to a DataFrame
df = pd.DataFrame(data)

# Load data into Surprise dataset format
reader = Reader(rating_scale=(1, 5))
dataset = Dataset.load_from_df(df[['user_id', 'item_id', 'rating']], reader)

# Split data into training and test sets
trainset, testset = train_test_split(dataset, test_size=0.2)
# Build the SVD model
model = SVD()

# Train the model
model.fit(trainset)

# Make predictions
predictions = model.test(testset)

# Evaluate the model performance
accuracy.rmse(predictions)
# Function to get recommendations for a specific user
def get_top_n(predictions, n=3):
    top_n = {}
    for uid, iid, true_r, est, _ in predictions:
        if uid not in top_n:
            top_n[uid] = []
        top_n[uid].append((iid, est))

    # Sort and return the top n recommendations for each user
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]
    return top_n

# Get top 3 recommendations for each user
top_n = get_top_n(predictions, n=3)

# Print top 3 recommendations for each user
for uid, user_ratings in top_n.items():
    print(f"User {uid} recommendations: {user_ratings}")
