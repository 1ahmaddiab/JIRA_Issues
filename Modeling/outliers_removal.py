
# coding: utf-8

# In[ ]:

import numpy as np

# It replaces outliers with NaNs.
def remove_outliers(df, column_name, multiplier=1.5):
    """
    Replaces outliers from a specific column in a DataFrame with NaNs based on the IQR method.
    
    Outliers are defined as values that fall below Q1 - 1.5*IQR or above Q3 + 1.5*IQR.

    Parameters:
    df (pandas.DataFrame): The input DataFrame from which outliers will be removed.
    column_name (str): The name of the column in the DataFrame for which outliers will be identified.
    multiplier (float, optional): The multiplier for the IQR. Default is 1.5.

    Returns:
    pandas.DataFrame: A new DataFrame with the outliers replaced with NaNs and will be removed in the prediction function.
    """

    # Calculate the IQR of the column
    IQR = df[column_name].quantile(0.75) - df[column_name].quantile(0.25)

    # Define the upper and lower bounds for outliers
    lower_bound = df[column_name].quantile(0.25) - multiplier * IQR
    upper_bound = df[column_name].quantile(0.75) + multiplier * IQR

    # Create a copy of df
    df_copy = df.copy()

    # Replace outliers in df_copy with NaN
    df_copy.loc[(df_copy[column_name] < lower_bound) | (df_copy[column_name] > upper_bound), column_name] = np.nan

    return df_copy


