import pandas as pd
import joblib

# Load the trained model
model = joblib.load("ml/classification/model.joblib")

# Example input data — structure must match the features used during training
# Let's say the model was trained on: ['quantity', 'unitprice', 'country'], which are not
# the features we used for training our model, so we will bump into an error.
# sample_data = pd.DataFrame(
#     [
#         {"quantity": 10, "unitprice": 200.0, "country": "united kingdom"},
#         {"quantity": 1, "unitprice": 2.5, "country": "france"},
#         {"quantity": 100, "unitprice": 15.0, "country": "germany"},
#     ]
# )

# Input sample — match training feature columns
sample_data = pd.DataFrame(
    [
        {"total_amount": 2000.0, "product_count": 10},
        {"total_amount": 2.5, "product_count": 1},
        {"total_amount": 1500.0, "product_count": 100},
    ]
)

# Predict class (0 = not high value, 1 = high value)
predictions = model.predict(sample_data)

# Attach predictions to the original data
sample_data["is_high_value"] = predictions

print(sample_data)
