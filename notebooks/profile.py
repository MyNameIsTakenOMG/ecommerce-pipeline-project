# profiling.py

import pandas as pd
from ydata_profiling import ProfileReport

# Load dataset (use the same CSV you used for recommendation)
df = pd.read_csv("../ml/recommendation/user_item_interactions.csv")

# Generate profile
profile = ProfileReport(df, title="User-Item Interactions Profile", explorative=True)

# Save report
profile.to_file("profiling_report.html")

print("✅ Profile report saved as profiling_report.html")
