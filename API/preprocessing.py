
# coding: utf-8

# In[2]:


from sklearn.preprocessing import LabelEncoder
import pandas as pd
from outliers_removal import remove_outliers


def preprocess_data(df):
    """
    Preprocesses a DataFrame containing issue data.

    This function performs various data transformations and encoding techniques to prepare the data for machine learning models.
    It creates a new DataFrame with the preprocessed data and returns it as the output.

    Parameters:
        df (pandas.DataFrame): The input DataFrame containing the raw issue data.
            It should have the following columns: 'key', 'status', 'priority', 'issue_type', 'created', 'updated',
            'description_length', 'summary_length', 'watch_count', 'comment_count', and 'resolutiondate'.

    Returns:
        pandas.DataFrame: The preprocessed DataFrame with the transformed and encoded data.

    Steps:
        1. Select a subset of the input DataFrame, `df`, including only the necessary columns for preprocessing.
        2. Define the list of columns that contain datetime data.
        3. Convert the datetime columns in the DataFrame to datetime format and format the datetime objects as strings in the format 'YYYY-MM-DD HH:MM:SS'.
        4. Convert the remaining object columns ('created', 'updated', 'resolutiondate') to datetime format.
        5. Calculate the time difference in seconds between 'resolutiondate' and 'created', and convert it to days, storing it in a new column 'days_since_created'.
        6. Extract additional features from the 'created' column: 'created_day_name' (day of the week), 'created_is_weekend' (whether it's a weekend or weekday), and 'created_month_name'.
        7. Replace 'Closed' status with 'Resolved', as the 'resolutiondate' for 'Closed' statuses represents the date when the issue is resolved.
        8. Perform ordinal encoding on categorical columns using predefined order mappings.
        9. Perform one-hot encoding on the 'issue_type' column using `LabelEncoder`.
        10. Drop the original categorical and date columns from the DataFrame.
        11. Return the preprocessed DataFrame, `df_issues`, as the output.

    Note:
        - The function assumes that the necessary modules, such as `pandas` and `sklearn.preprocessing.LabelEncoder`, are imported before calling the function.
    """
  
    # Create a new DataFrame from a subset of df, selecting only the needed columns
    df_issues = df[['key', 'status', 'priority', 'issue_type', 'created', 'updated', 'description_length', 'summary_length', 'watch_count', 'comment_count', 'resolutiondate']].copy()

    # Define the list of columns that contain datetime data
    datetime_columns = ['created', 'updated', 'resolutiondate']

    # Loop over the datetime columns
    for column in datetime_columns:
        # Convert the column in df_issues to datetime format
        df_issues[column] = pd.to_datetime(df_issues[column])
        # Format the datetime objects as strings in the format 'YYYY-MM-DD HH:MM:SS'
        df_issues[column] = df_issues[column].dt.strftime('%Y-%m-%d %H:%M:%S')

    # Convert object columns to datetime
    df_issues['created'] = pd.to_datetime(df_issues['created'])
    df_issues['updated'] = pd.to_datetime(df_issues['updated'])
    df_issues['resolutiondate'] = pd.to_datetime(df_issues['resolutiondate'])

    # Calculate the time difference in seconds
    time_difference = (df_issues['resolutiondate'] - df_issues['created']).dt.total_seconds()
    # Convert the time difference to days
    df_issues['days_since_created'] = (time_difference / (24 * 60 * 60)).round()

    # Extract day name
    df_issues['created_day_name'] = df_issues['created'].dt.day_name()
    # Extract whether the day is a weekend or weekday
    df_issues['created_is_weekend'] = df_issues['created'].dt.weekday >= 5
    # Extract month name
    df_issues['created_month_name'] = df_issues['created'].dt.month_name()

    # Since the resolutiondate for Closed statuses is the date when the issue is resolved, Closed is replaced by Resolved
    df_issues['status'] = df_issues['status'].replace('Closed', 'Resolved')

    # Ordinal encoding
    status_order = ['Open', 'Patch Available', 'In Progress', 'Resolved', 'Reopened', 'Closed']
    priority_order = ['Trivial', 'Minor', 'Major', 'Critical', 'Blocker']
    created_day_name_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    created_month_name_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    ordinal_mapping = {
        'status': status_order,
        'priority': priority_order,
        'created_day_name': created_day_name_order,
        'created_month_name': created_month_name_order
    }

    for column, order in ordinal_mapping.items():
        df_issues[column] = pd.Categorical(df_issues[column], categories=order, ordered=True)
        df_issues[column] = df_issues[column].cat.codes + 1
        df_issues[column] = df_issues[column].astype('int64')  # Convert the column to int64 here

    # One-hot encoding for the nominal category
    encoder = LabelEncoder()
    df_issues['issue_type'] = encoder.fit_transform(df_issues['issue_type'])

    # Drop the original categorical and date columns
    df_issues.drop(['key', 'created', 'resolutiondate', 'updated', 'created_is_weekend'], axis=1, inplace=True)
    
    # Replaces outliers with NaNs (will be removed in the prediction function)
    df_issues_without_days_outliers = remove_outliers(df_issues, 'days_since_created', multiplier=1.5)
    
    return df_issues_without_days_outliers

