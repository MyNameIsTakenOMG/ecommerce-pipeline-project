import joblib
import pandas as pd
from scipy.sparse import coo_matrix

# Load model and mappings
model = joblib.load("ml/recommendation/model/als_model.joblib")
user_mapping = joblib.load("ml/recommendation/model/user_mapping.joblib")
item_mapping = joblib.load("ml/recommendation/model/item_mapping.joblib")
user_inverse_mapping = joblib.load(
    "ml/recommendation/model/user_inverse_mapping.joblib"
)
item_inverse_mapping = joblib.load(
    "ml/recommendation/model/item_inverse_mapping.joblib"
)

# Build dummy user_items interaction vector (1 row, all columns = 0)
user_vector = coo_matrix(([], ([], [])), shape=(1, len(item_mapping))).tocsr()

# Choose a known customer ID
input_customer_id = 12347.0  # update this based on your dataset

# # Load interaction data (same as during training)
# df = pd.read_csv("ml/recommendation/user_item_interactions.csv")
# df["CustomerID"] = df["CustomerID"].astype(float)  # make sure it's consistent
# df["StockCode"] = df["StockCode"].astype(str)

# # Rebuild user-item sparse matrix
# user_ids = df["CustomerID"].astype("category")
# item_ids = df["StockCode"].astype("category")

# matrix = coo_matrix(
#     (
#         df["TotalQuantity"].astype(float),
#         (item_ids.cat.codes, user_ids.cat.codes),
#     )
# ).tocsr()  # Convert to CSR format

# Check and map to ALS internal ID
if input_customer_id not in user_inverse_mapping:
    raise ValueError(f"Customer ID {input_customer_id} not found in training data.")

user_internal_id = user_inverse_mapping[input_customer_id]

# # Extract the user interaction vector (in CSR format)
# user_vector = matrix[:, user_internal_id].T.tocsr()

# Generate top-5 recommendations
# recommendations = model.recommend(
item_ids, scores = model.recommend(
    userid=user_internal_id,
    user_items=user_vector,
    N=5,
)

print("Item IDs returned by model:", item_ids)
print("Scores:", scores)

# Print the results
print(f"Top 5 recommendations for customer {input_customer_id}:")
# print(recommendations)

# recommendations: a tuple of two arrays:
# - item_internal_id: the internal ID of the recommended item
# - score: the predicted score for that item

# print(item_mapping.keys())

for item_internal_id, score in zip(item_ids, scores):
    item_code = item_mapping[int(item_internal_id)]
    print(f"Product: {item_code}, Score: {score:.2f}")
