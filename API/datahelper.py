import pandas as pd

# Read the tracking issue CSV file located in data folder
avro_issues = pd.read_csv('../data/avro-issues.csv')


def get_issue_by_key(issue_key):
    # Get the issue key from the non resolved data (csv)
    issue = avro_issues[avro_issues['key'] == issue_key]
    return issue


def get_avro_issues_data():
    return avro_issues


def get_issues_till_date(df, date):
    unresolved_issues = df[~df['status'].isin(['Resolved', 'Closed'])]

    unresolved_issues_copy = unresolved_issues.copy()
    unresolved_issues_copy.loc[:, 'created'] = pd.to_datetime(unresolved_issues_copy['created'])

    date_cutoff = pd.to_datetime(date)
    filtered_df = unresolved_issues_copy[unresolved_issues_copy['created'] <= date_cutoff]
    return filtered_df



