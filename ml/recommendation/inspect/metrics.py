# # inspect/metrics.py

# import pandas as pd
# import numpy as np
# import joblib
# from sklearn.model_selection import train_test_split
# from collections import defaultdict

# # Load model and mappings
# model = joblib.load("ml/recommendation/model/als_model.joblib")
# user_mapping = joblib.load("ml/recommendation/model/user_mapping.joblib")
# item_mapping = joblib.load("ml/recommendation/model/item_mapping.joblib")
# interaction_df = pd.read_csv("ml/recommendation/user_item_interactions.csv")
# print("Original interaction_df size:", len(interaction_df))
# print(interaction_df.head())
# # Map IDs
# interaction_df["user_idx"] = interaction_df["CustomerID"].map(user_mapping)
# interaction_df["item_idx"] = interaction_df["StockCode"].map(item_mapping)
# print("Unique CustomerIDs mapped:", interaction_df["user_idx"].nunique())
# print("Unique StockCodes mapped:", interaction_df["item_idx"].nunique())
# print("interaction_df size after mapping:", len(interaction_df))

# # Drop unknowns
# interaction_df.dropna(subset=["user_idx", "item_idx"], inplace=True)
# interaction_df = interaction_df.astype({"user_idx": int, "item_idx": int})

# # Train-test split
# train_df, test_df = train_test_split(interaction_df, test_size=0.2, random_state=42)

# # Build ground-truth dictionary
# ground_truth = defaultdict(set)
# for row in test_df.itertuples():
#     ground_truth[row.user_idx].add(row.item_idx)


# # Get top-K recommendations for each user
# def get_top_k_recs(model, user_ids, k=10):
#     recs = {}
#     for user_id in user_ids:
#         try:
#             user_recs = model.recommend(user_id, k=k)
#             recs[user_id] = set([item_id for item_id, _ in user_recs])
#         except:
#             recs[user_id] = set()
#     return recs


# # Evaluation metrics
# def recall_at_k(recs, ground_truth, k):
#     recalls = []
#     for user in ground_truth:
#         true_items = ground_truth[user]
#         pred_items = recs.get(user, set())
#         recalls.append(
#             len(true_items & pred_items) / len(true_items) if true_items else 0
#         )
#     return np.mean(recalls)


# def apk(actual, predicted, k=10):
#     if len(predicted) > k:
#         predicted = predicted[:k]

#     score = 0.0
#     num_hits = 0.0

#     for i, p in enumerate(predicted):
#         if p in actual and p not in predicted[:i]:
#             num_hits += 1.0
#             score += num_hits / (i + 1.0)

#     return score / min(len(actual), k) if actual else 0.0


# def mapk(recs, ground_truth, k=10):
#     scores = []
#     for user in ground_truth:
#         actual = list(ground_truth[user])
#         predicted = list(recs.get(user, []))
#         scores.append(apk(actual, predicted, k))
#     return np.mean(scores)


# # Run evaluation
# top_k = 10
# user_ids = list(ground_truth.keys())
# recs = get_top_k_recs(model, user_ids, k=top_k)

# recall = recall_at_k(recs, ground_truth, k=top_k)
# map_score = mapk(recs, ground_truth, k=top_k)

# print(f"Recall@{top_k}: {recall:.4f}")
# print(f"MAP@{top_k}: {map_score:.4f}")

import pandas as pd

df = pd.read_csv("ml/recommendation/user_item_interactions.csv")
print(df["CustomerID"].dtype)
print(df["CustomerID"].head())
