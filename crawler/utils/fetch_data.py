import csv

import pandas as pd


def get_comment_count_from_booking(json_string):
    comment_count = json_string['data']['reviewListFrontend']['reviewsCount']
    return comment_count


def get_comments_from_booking(json_string):
    original_comments = json_string['data']['reviewListFrontend']['reviewCard']
    # 提取textDetails和partnerReply字段
    comments = []
    for comment in original_comments:
        comments.append({
            "textDetails": comment.get("textDetails"),
            "partnerReply": comment.get("partnerReply")
        })
    return comments


def get_comments_count_from_airbnb(json_string):
    comments_count = json_string['data']['presentation']['stayProductDetailPage']['reviews']['metadata'][
        'reviewsCount']
    return comments_count