
import numpy as np
import pandas as pd

df = pd.read_json(r"data/regItems.json")
df = df.replace(to_replace="", value=np.nan).dropna(axis=0) # remove null values
df['paragraphText'] = df['paragraphText'].str.replace("OLD SECTION.*", "", regex=True) # remove any dirty words
# df['paragraphText'] = df['paragraphText'].str.replace("[a-zA-z]\d\w+", ". ", regex=True)
df['paragraphText'] = df['paragraphText'].str.lower()

data = df['paragraphText'].tolist()