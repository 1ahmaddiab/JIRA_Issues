
# coding: utf-8

# In[2]:


import unittest
import pandas as pd
from predict import predict_resolution_date
import datetime

class TestPredictResolutionDate(unittest.TestCase):
    """
    Methods:
        - setUp: Method to set up the test environment before each test case.
        - test_predict_resolution_date_with_key_none: Method to test the function with key=None.
        - test_predict_resolution_date_with_specific_key: Method to test the function with a specific key.
    """

    def setUp(self):
        """
        Method to set up the test environment before each test case.

        Reads the raw data and the expected dataframe from CSV.
        Converts the dtype of 'days_since_created' column in the expected dataframe.
        """

        # Read the raw data from CSV
        self.df_avro_issues = pd.read_csv('../data/for testing df_avro_issues raw data.csv')

        # Read the expected dataframe from CSV
        self.final_resolution_date_df = pd.read_csv('../data/for testing final_resolution_date_df after predicting.csv')


    def test_predict_resolution_date_with_key_none(self):
        """
        Method to test the predict_resolution_date function with key=None.

        Compares the returned result with the expected result for key=None.
        """
        
        # Expected result for key=None
        expected_result = self.final_resolution_date_df

        result = predict_resolution_date(self.df_avro_issues, key=None)

        # Define the list of columns that contain datetime data
        datetime_columns = ['created', 'updated', 'resolutiondate']

        # Convert the datetime columns to datetime format and format them as strings
        expected_result[datetime_columns] = expected_result[datetime_columns].apply(
            lambda x: x.apply(lambda y: pd.to_datetime(y).strftime('%Y-%m-%d')), axis=1
        )
        # Convert the datetime columns to datetime format and format them as strings
        result[datetime_columns] = result[datetime_columns].apply(
            lambda x: x.apply(lambda y: pd.to_datetime(y).strftime('%Y-%m-%d')), axis=1
        )

        # Drop 'days_since_created' column from both dataframes
        result = result.drop(columns='days_since_created')
        expected_result = expected_result.drop(columns='days_since_created')

        self.assertTrue(isinstance(result, pd.DataFrame))
        pd.testing.assert_frame_equal(result, expected_result, check_exact=False)



    def test_predict_resolution_date_with_specific_key(self):
        """
        Method to test the predict_resolution_date function with a specific key.

        Compares the returned result with the expected result for a specific key.
        """

        # Expected result for key='AVRO-2171'
        expected_result = '2018-04-24 07:30:24'

        result = predict_resolution_date(self.df_avro_issues, key='AVRO-2171')

        self.assertEqual(result, expected_result)
        # Assuming 'result' and 'expected_result' are datetime objects
        # self.assertAlmostEqual(result, expected_result, delta=datetime.timedelta(seconds=10))

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2, exit=False)

