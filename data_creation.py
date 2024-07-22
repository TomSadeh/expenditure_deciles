"""
This script performs the following tasks:

Library Imports:
Imports the necessary libraries: pandas for data manipulation, numpy for numerical operations, and DescrStatsW from statsmodels for weighted descriptive statistics.

Data Loading:
Reads a CSV file containing the 2022 Expenditure Survey data into a DataFrame named mbs.
Converts all column names to lowercase for consistency.

DataFrame Initialization:
Initializes an empty DataFrame named results with an index corresponding to decile limits (from 0.1 to 0.9).

Quantile Calculation:
Calculates the quantiles for each category (columns 'c30' to 'c39') weighted by the 'weight' column, and normalizes these values by dividing by 'nefeshstandartit'.
Stores these quantile values in the results DataFrame.

Upper Limit Adjustment:
Adds an open upper limit for the 10th decile by setting the value for index 1.0 to be the value of the 9th decile (0.9) plus 1.
"""

# Importing the required libraries.
import pandas as pd
import numpy as np
from statsmodels.stats.weightstats import DescrStatsW as dsw

# Importing the 2022 Expenditure Survey
mbs = pd.read_csv(r"C:\Backup\CBS Households Expenditures Survey\famexp_2022\H20221021datamb.csv")
mbs.columns = mbs.columns.str.lower()

# Creating an empty DataFrame to contain the results of the deciles limits.
results = pd.DataFrame(index=np.round(np.arange(0.1,1,step=0.1), 1))

# Calculating the limits of each category.
results = dsw(mbs.loc[:, 'c30' : 'c39'].div(mbs['nefeshstandartit'], axis=0), mbs['weight']).quantile(np.round(np.arange(0.1,1,step=0.1), 1))

# Creating an open upper limit of the 5th     
results.loc[1.0, :] = results.loc[0.9, :] + 1   

