import pandas as pd
import os


path = "data/raw"


files = os.listdir(path)


for file in files:

    if file.endswith(".csv"):

        print("\n====================")
        print(file)

        df = pd.read_csv(
            os.path.join(path, file)
        )

        print(df.head())

        print("\nColumns:")
        print(df.columns.tolist())

        print("\nShape:")
        print(df.shape)