
# coding: utf-8

# In[ ]:

from sklearn.externals import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from preprocessing import preprocess_data
import numpy as np

def predict_resolution_date(df_avro_issues, key=None):
    """
    Predict the resolution date of an issue or a DataFrame of issues based on its key using a pre-trained Random Forest regression model.

    If a specific key is provided, this function returns the predicted resolution date for that specific issue.
    If no key is provided, this function returns a DataFrame of all issues along with their predicted resolution dates.

    Parameters:
    df_avro_issues (pd.DataFrame): A DataFrame containing the issues data. Each row corresponds to a specific issue.
                                   Necessary columns are 'days_since_created', 'status', and 'created'.
    key (str, optional): The key of the issue for which the resolution date should be predicted. If not provided,
                         the function returns the entire DataFrame with predicted resolution dates.

    Returns:
    str or pd.DataFrame: The predicted resolution date for the issue in the format 'YYYY-MM-DD HH:MM:SS', 
                         or the entire DataFrame with predicted resolution dates if 'key' is not provided.

    Notes:
    The preprocessing of the data is done using the 'preprocess_data' function from a module named 'preprocessing'.
    """
        

    # To load the Random Forest Regressor model
    loaded_model = joblib.load('../RF_regressor_model.pkl')


    # Load the new preprocessed dataset
    filtered_preprocessed_df = preprocess_data(df_avro_issues)

    pred_preprocessed_df = filtered_preprocessed_df[filtered_preprocessed_df['status'] != 4].drop(['days_since_created', 'status'], axis=1)


    # Handling NaNs (here some NaNs may exist in the description length feature)
    pred_preprocessed_df = pred_preprocessed_df.fillna(pred_preprocessed_df.mean())


    # Declare final_resolution_date_df as global
    global final_resolution_date_df
    
    
    # Predicting the results for new dataset
    predictions = loaded_model.predict(pred_preprocessed_df)
    

    # copy the raw dataset and add the predicted days_since_created for the unresolved issues
    final_resolution_date_df = df_avro_issues.copy()
    
    # Add a new column to the preprocessed DataFrame with the predictions
    pred_preprocessed_df['days_since_created'] = predictions

    
    final_resolution_date_df = final_resolution_date_df.merge(pred_preprocessed_df[['days_since_created']], how='left', left_index=True, right_index=True)


    # Convert 'resolutiondate' and 'created' to datetime
    final_resolution_date_df['resolutiondate'] = pd.to_datetime(final_resolution_date_df['resolutiondate'])
    final_resolution_date_df['created'] = pd.to_datetime(final_resolution_date_df['created'])

    # Calculate the time difference in seconds for rows where 'days_since_created' is NaN
    mask = final_resolution_date_df['days_since_created'].isna()
    time_difference = (final_resolution_date_df.loc[mask, 'resolutiondate'] - final_resolution_date_df.loc[mask, 'created']).dt.total_seconds()

    # Convert the time difference to days with fraction
    final_resolution_date_df.loc[mask, 'days_since_created'] = (time_difference / (24 * 60 * 60)).round()

    
    
    
  
    #     # Make sure 'created' is datetime and 'days_since_created' is timedelta to add them to get resolutiondate datetime
    #     final_resolution_date_df['created'] = pd.to_datetime(final_resolution_date_df['created'])
    #     final_resolution_date_df['days_since_created'] = pd.to_timedelta(final_resolution_date_df['days_since_created'], unit='D')

    # Make sure 'created' is datetime and 'days_since_created' is timedelta to add them to get resolutiondate datetime
    # final_resolution_date_df['created'] = pd.to_datetime(final_resolution_date_df['created'])
    final_resolution_date_df['days_since_created'] = pd.to_timedelta(final_resolution_date_df['days_since_created'], unit='D')


    # Convert 'created' column to string
    final_resolution_date_df['created'] = final_resolution_date_df['created'].astype(str)

    # Split the string on the dot and take the first part
    final_resolution_date_df['created'] = final_resolution_date_df['created'].str.split('.').str[0]

    # Convert the string back to datetime format
    final_resolution_date_df['created'] = pd.to_datetime(final_resolution_date_df['created'])

    final_resolution_date_df['days_since_created'] = pd.to_timedelta(
        final_resolution_date_df['days_since_created']
        .dt
        .total_seconds()
        .astype(int)
        .astype('timedelta64[s]')
    )
    
    # Convert 'resolutiondate' column to datetime
    final_resolution_date_df['resolutiondate'] = pd.to_datetime(final_resolution_date_df['resolutiondate'])

    # Check if 'resolutiondate' is NaN
    mask = pd.isna(final_resolution_date_df['resolutiondate'])

    # Add the timedelta to 'created' and assign the result to 'resolutiondate' where 'resolutiondate' is NaN
    final_resolution_date_df.loc[mask, 'resolutiondate'] = final_resolution_date_df['created'] + final_resolution_date_df['days_since_created']    


    # Define the list of columns that contain datetime data
    datetime_columns = ['created', 'updated', 'resolutiondate']

    # Convert the datetime columns to datetime format and format them as strings
    final_resolution_date_df[datetime_columns] = final_resolution_date_df[datetime_columns].apply(
        lambda x: x.apply(lambda y: pd.to_datetime(y).strftime('%Y-%m-%d %H:%M:%S')), axis=1
    )

    
#     # add 'days_since_created' to 'created' where 'resolutiondate' is NaT
#     final_resolution_date_df.loc[final_resolution_date_df['resolutiondate'].isna(), 'resolutiondate'] = final_resolution_date_df['created'] + final_resolution_date_df['days_since_created']

#     # Define the list of columns that contain datetime data
#     datetime_columns = ['created', 'updated', 'resolutiondate']
#     # # Convert the datetime columns to datetime format and format them as strings
#     # final_resolution_date_df[datetime_columns] = final_resolution_date_df[datetime_columns].apply(pd.to_datetime).apply(lambda x: x.dt.strftime('%Y-%m-%d %H:%M:%S'))

#     for col in datetime_columns:
#         final_resolution_date_df[col] = pd.to_datetime(final_resolution_date_df[col])
#         final_resolution_date_df[col] = final_resolution_date_df[col].dt.strftime('%Y-%m-%d %H:%M:%S')


    if key is None:
        return final_resolution_date_df
    else:
        return final_resolution_date_df.loc[final_resolution_date_df['key'] == key, 'resolutiondate'].values[0]
    
    