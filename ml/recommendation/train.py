import pandas as pd
from implicit.als import AlternatingLeastSquares
from scipy.sparse import coo_matrix
import joblib
import os

# Load interaction data
df = pd.read_csv("ml/recommendation/user_item_interactions.csv")

# Clean CustomerID and StockCode columns
df = df[df["CustomerID"].notna()]
df = df[df["StockCode"].notna()]
df["StockCode"] = df["StockCode"].astype(str).str.strip()

# Optional: keep only alphanumeric stock codes
df = df[df["StockCode"].str.match(r"^[A-Za-z0-9]+$")]

# Filter out any zero or negative quantities --> without filtering, we would bump into issues such as:
#     item_code = item_mapping[int(item_internal_id)]
#                ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
#      KeyError: 3888
# because some items may get skipped implicitly during the training process for bad data
df = df[df["TotalQuantity"] > 0]

# Create mappings for user and item IDs
user_ids = df["CustomerID"].astype("category")
item_ids = df["StockCode"].astype("category")

# Save mappings to restore later during inference
user_mapping = dict(enumerate(user_ids.cat.categories))
item_mapping = dict(enumerate(item_ids.cat.categories))
user_inverse_mapping = {v: k for k, v in user_mapping.items()}
item_inverse_mapping = {v: k for k, v in item_mapping.items()}

# Create sparse matrix (items x users) for implicit library
matrix = coo_matrix(
    (
        df["TotalQuantity"].astype(float),
        (item_ids.cat.codes, user_ids.cat.codes),
    )
)

# Train ALS model
model = AlternatingLeastSquares(
    factors=50,  # number of latent factors (dimensions of embeddings). Think of this like embedding size — it controls how much nuance the model can capture. More = more expressive, but slower.
    regularization=0.1,  # Prevents overfitting by penalizing large feature weights.
    iterations=20,  # Number of times ALS alternates between users and items = better convergence but more time.
    use_gpu=False,  # GPU support available with optional libraries
)

# Fit the model
model.fit(matrix)

# Save the model and mappings
os.makedirs("ml/recommendation/model", exist_ok=True)
joblib.dump(model, "ml/recommendation/model/als_model.joblib")
joblib.dump(user_mapping, "ml/recommendation/model/user_mapping.joblib")
joblib.dump(item_mapping, "ml/recommendation/model/item_mapping.joblib")
joblib.dump(user_inverse_mapping, "ml/recommendation/model/user_inverse_mapping.joblib")
joblib.dump(item_inverse_mapping, "ml/recommendation/model/item_inverse_mapping.joblib")

print(f"Total ALS item IDs: {model.item_factors.shape[0]}")
print(f"Item mapping size: {len(item_mapping)}")
print("ALS model training completed and saved.")
