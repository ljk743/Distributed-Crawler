import json
import re

import pandas as pd
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


def airbnb_csv(input_path, output_path):
    """
    Extracts English reviews from an Airbnb JSON file, cleans them by removing HTML tags,
    and saves the results to a CSV file.

    Args:
        input_path (str): Path to the input JSON file containing Airbnb reviews.
        output_path (str): Path where the output CSV file with cleaned reviews will be saved.
    """
    # Load the JSON data from the input file
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Recursive function to extract English reviews from the nested JSON structure
    def recursive_extract(data, reviews):
        if isinstance(data, dict):
            # Check if the dictionary has a type identifier
            if "__typename" in data:
                typename = data["__typename"]
                # If the type is 'PdpReviewForP3' and the review is in English, extract the comments
                if typename == "PdpReviewForP3":
                    if "comments" in data and "language" in data and data["language"] == "en":
                        reviews.append(data["comments"])
                # If the type is 'LocalizedReview', extract the comments
                elif typename == "LocalizedReview":
                    if "comments" in data:
                        reviews.append(data["comments"])
            # Recursively call this function for all dictionary values
            for key, value in data.items():
                recursive_extract(value, reviews)
        elif isinstance(data, list):
            # If the data is a list, recursively process each item in the list
            for item in data:
                recursive_extract(item, reviews)

    # Function to remove HTML tags from the extracted comments
    def remove_html_tags(text):
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    reviews = []  # Initialize an empty list to store the extracted reviews
    recursive_extract(data, reviews)  # Start the extraction process

    # Clean the reviews by removing any HTML tags
    cleaned_reviews = [remove_html_tags(review) for review in reviews]

    # Save the cleaned reviews to a CSV file
    df = pd.DataFrame({
        "sentence": cleaned_reviews  # Create a DataFrame with a single column 'sentence'
    })
    df.to_csv(output_path, index=False, quoting=1)  # Save the DataFrame to a CSV file
    print(f"English reviews have been extracted and saved to {output_path}")


def booking_csv(input_path, output_path):
    """
    Extracts positive and negative reviews from a Booking.com JSON file, cleans them,
    and saves the results to a CSV file.

    Args:
        input_path (str): Path to the input JSON file containing Booking.com reviews.
        output_path (str): Path where the output CSV file with cleaned reviews will be saved.
    """

    # Function to clean the text by removing special characters, converting to lowercase,
    # and removing stopwords
    def clean_text(text):
        if text is None:
            return ''
        text = re.sub(r'[\r\n]+', ' ', text)  # Merge multiple lines into one
        text = re.sub(r'[^\w\s.,!?]', '', text)  # Remove special characters and emojis
        text = text.lower()  # Convert text to lowercase
        text = ' '.join(word for word in text.split() if word not in ENGLISH_STOP_WORDS)
        return text

    # Load the JSON data from the input file
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    reviews = []  # Initialize an empty list to store the extracted reviews

    # Iterate through each entry in the JSON data to extract and clean reviews
    for entry in data:
        text_details = entry.get('textDetails', {})
        positive_text = text_details.get('positiveText')
        negative_text = text_details.get('negativeText')

        # Validate and clean the positive review text
        if positive_text and positive_text.lower() != 'n/a' and positive_text.strip() != '':
            if positive_text.lower() != 'nothing.' or 'nothing!':
                positive_text_cleaned = clean_text(positive_text)
                reviews.append(positive_text_cleaned)

        # Validate and clean the negative review text
        if negative_text and negative_text.lower() != 'n/a' and negative_text.strip() != '':
            if negative_text.lower() != 'nothing.' or 'nothing!':
                negative_text_cleaned = clean_text(negative_text)
                reviews.append(negative_text_cleaned)

    # Convert the list of cleaned reviews to a DataFrame with a single column 'sentence'
    df = pd.DataFrame(reviews, columns=['sentence'])

    # Remove any empty rows from the DataFrame
    df = df[df['sentence'].str.strip() != '']

    # Save the cleaned reviews to a CSV file
    df.to_csv(output_path, index=False, quoting=1, lineterminator='\n')
    print(f"Reviews have been extracted and saved to {output_path}")
