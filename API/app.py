import os

from flask import Flask, jsonify
from predict import predict_resolution_date

from datahelper import get_issue_by_key
from datahelper import get_avro_issues_data
from datahelper import get_issues_till_date



app = Flask(__name__)

@app.route('/api/issue/<issue_key>/resolve-fake3', methods=['GET'])
def resolve_fake3(issue_key):
    return jsonify({
        'issue': issue_key,
        'predicted_resolution_date': '1970-01-01T00:00:00.000+0000'
    })



@app.route('/api/issue/<issue_key>/resolve-prediction', methods=['GET'])
def resolve_predict(issue_key):
    issue = get_issue_by_key(issue_key)
    # Check if the issue key exists in the data
    if issue.empty:
        return jsonify({'error': 'Issue key not found'}), 404

    resolution_date = predict_resolution_date(issue, issue_key)
    return jsonify({
        'issue': issue_key,
        'predicted_resolution_date': resolution_date
    })



@app.route('/api/release/<date>/resolved-since-now', methods=['GET'])
def resolved_since_now(date):
    avro_issues = get_avro_issues_data()
    predicted_issues = predict_resolution_date(avro_issues)
    filtered_df = get_issues_till_date(predicted_issues, date)
    # Construct a list of issues with their predicted resolution dates
    issues = [
        {
            'issue': row['key'],
            'predicted_resolution_date': row['created']
        }
        for _, row in filtered_df.iterrows()
    ]

    return jsonify({
        'now': date,
        'issues': issues
    })


