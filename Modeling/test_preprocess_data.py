
# coding: utf-8

# In[5]:


from preprocessing import preprocess_data
import unittest
import pandas as pd

class TestPreprocessData(unittest.TestCase):
    """
    Methods:
        - setUp: Method to set up the test environment before each test case.
        - test_preprocess_data: Method to test the preprocess_data function.
    """

    def setUp(self):
        """
        Method to set up the test environment before each test case.

        Reads the raw data from CSV and the expected preprocessed dataframe from CSV.
        """

        # Read the raw data from CSV
        self.df_avro_issues = pd.read_csv('../data/for testing df_avro_issues raw data.csv')

        # Read the expected dataframe from CSV
        self.preprocessed_df = pd.read_csv('../data/for testing preprocessed_df after preprocessing.csv')

    def test_preprocess_data(self):
        """
        Method to test the preprocess_data function.

        Applies the preprocess_data function to the input raw data.
        Compares the result to the expected preprocessed dataframe.
        """
        # Apply the preprocess_data function to input raw data
        result_df = preprocess_data(self.df_avro_issues)

        # Compare the result to the expected output
        # pd.testing.assert_frame_equal(result_df, self.preprocessed_df)
        pd.testing.assert_frame_equal(result_df.reset_index(drop=True), 
                              self.preprocessed_df.reset_index(drop=True), 
                              check_dtype=False)



if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2, exit=False)

