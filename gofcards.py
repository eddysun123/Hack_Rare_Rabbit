# -*- coding: utf-8 -*-
"""GoFCards.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VJIoH2LmpYFXsvXQUwr1fWMHcsJsHrXU

## GoFCards Database

Reference Paper: https://academic.oup.com/nar/article/53/D1/D976/7907365

Database: https://www.genemed.tech/gofcards/#/index/home
"""

import pandas as pd
import numpy as np

###############################################################################
# 1) Read Excel File
###############################################################################
df = pd.read_excel("gofcards_data_download.xlsx")  # Update filename/path if needed

###############################################################################
# 2) Log Normalization of Pscore
def log_normalize_pscore(pscore, max_pscore):
    """ Normalize Pscore using log transformation (scaled 0-1). """
    if pd.isna(pscore) or pscore <= 0:
        return 0
    return np.log2(1 + pscore) / np.log2(1 + max_pscore)

###############################################################################
# 3) Apply Transformations to DataFrame
###############################################################################

# -- Get Max Pscore Value for Normalization --
max_pscore = df["Pscore"].max()

# -- Assign GoF = 1 for ALL ENTRIES (since this is GoFCards) --
df["LoF"], df["GoF"], df["DN"] = 0, 1, 0

# -- Normalize Pscore using Log Scaling --
df["Pscore_Normalized"] = df["Pscore"].apply(lambda x: log_normalize_pscore(x, max_pscore))

# -- Build 4D Vector <LoF, GoF, DN, Pscore_Normalized> --
df["Mechanism_Vector_4D"] = df.apply(
    lambda row: [row["LoF"], row["GoF"], row["DN"], row["Pscore_Normalized"]],
    axis=1
)

###############################################################################
# 4) Inspect & Export Processed Data
###############################################################################

print(df[[
    "genesymbol",
    "Disorder involved",
    "Pscore",
    "Pscore_Normalized",
    "LoF", "GoF", "DN",
    "Mechanism_Vector_4D"
]].head(20))

df.to_csv("processed_gofcards.csv", index=False)

print("✅ Processed data saved as 'processed_gofcards.csv'")