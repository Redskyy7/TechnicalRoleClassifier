# Github Issue Classifier

This project aims to classify GitHub issues into various categories based on the technologies used by contributors to a given repository. It uses data from the GitHub API, including contributor details, repository languages, and technologies used, to train a machine learning model that predicts the profile of developers based on the technologies they use.

## Features

- Fetches a list of contributors from a specified GitHub repository.
- Identifies technologies used by contributors in their repositories.
- Classifies developers into different profiles based on the technologies they use.
- Uses a Random Forest Classifier to predict developer profiles.
- Saves the results into an Excel file.

## Technologies

- Python
- Pandas
- Scikit-learn
- GitHub API
- OpenPyXL (for saving results as Excel)
