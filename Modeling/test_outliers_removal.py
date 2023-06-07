
# coding: utf-8

# In[9]:


# import the necessary libraries
from outliers_removal import remove_outliers
import unittest
import pandas as pd

# Define the test case class
class TestRemoveOutliers(unittest.TestCase):
    def setUp(self):
        """
        This method is used for test case setup. This will get called before every test method.
        
        Here, it reads the input and expected output data from csv files before each test.
        """
        # Load the encoded dataset before removing ourliers
        self.encoded_df_issues = pd.read_csv('../data/for testing encoded_df_issues before removing outliers.csv')

        # # Load the encoded dataset after removing ourliers
        self.no_outliers_encoded_df_issues = pd.read_csv('../data/for testing no_outliers_encoded_df_issues df after removing outliers.csv')

    # define a test method
    def test_remove_outliers(self):
        """
        This method tests the remove_outliers function by comparing the function's output 
        to an expected output.
        """
        # Apply the remove_outliers function to the input data
        result_df = remove_outliers(self.encoded_df_issues, 'days_since_created')

        # Compare the result to the expected output using testing assert function
        pd.testing.assert_frame_equal(result_df, self.no_outliers_encoded_df_issues)

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)

