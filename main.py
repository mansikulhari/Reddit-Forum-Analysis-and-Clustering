# -*- coding: utf-8 -*-
"""DSCI560 Assignment 4.ipynb
"""

import praw

# API id and secret key creation link: https://www.reddit.com/prefs/apps
reddit = praw.Reddit(client_id='yzjwJGWRC-Ej-ibYbQ5fAg',
                     client_secret='YmuI4saCK99aLecdtd51xYckDSGCFA',
                     user_agent='windows:DSCI560:v1 (by /u/TheDemonicJay)')  # Cringe old gaming tag, please don't
# judge too much

subreddit = reddit.subreddit('tech')

# Requests per Minute (RPM): Typically, the limit is around 60 requests per minute for most API endpoints. This means
# you can make up to 60 requests to the Reddit API per minute. Requests per Day (RPD): The daily limit can vary based
# on your application type (script, installed app, web app). For script-type applications, it's usually around 10,
# 000 requests per day. Quota: Reddit applies a quota system that replenishes at a set rate. For example,
# you might have a quota of 1000 requests every 10 minutes.

import pandas as pd


def top_posts(duration='month'):  # "all", "day", "hour", "month", "week", or "year"
    # Top posts for the specified duration
    posts = subreddit.top(duration)

    # Dictionary for storing the details
    posts_dict = {"ID": [],
                  "Title": [],
                  "Author": [],
                  "Post Text": [],
                  "Score": [],
                  "Upvote ratio": [],
                  "Total Comments": [],
                  "Post URL": [],
                  "Media": [],
                  }

    for post in posts:
        # Title of posts
        posts_dict["Title"].append(post.title)

        # User id
        posts_dict["Author"].append(post.author.name)

        # Text inside a post
        posts_dict["Post Text"].append(post.selftext)

        # Unique ID of each post
        posts_dict["ID"].append(post.id)

        # The score of a post
        posts_dict["Score"].append(post.score)

        # Upvote ratio of the post
        posts_dict["Upvote ratio"].append(post.upvote_ratio)

        # Total number of comments inside the post
        posts_dict["Total Comments"].append(post.num_comments)

        # URL of each post
        posts_dict["Post URL"].append(post.url)

        # Media
        posts_dict["Media"].append(post.media)

    # Saving the data in a pandas dataframe
    top_posts = pd.DataFrame(posts_dict)
    return top_posts


top_posts()


def comments(post_id):
    # Searching for all the comments of a post by its ID
    post = reddit.submission(id=post_id)

    comments_dict = {"ID": [],
                     "Body": [],
                     "Author": [],
                     "Score": [],
                     "Total replies": []
                     }

    for comment in post.comments[1:]:
        if comment.body == '[deleted]':
            continue
        # Body of comments
        comments_dict["Body"].append(comment.body)

        # User id
        comments_dict["Author"].append(comment.author.name)  # top

        # Unique ID of each comment
        comments_dict["ID"].append(comment.id)

        # The score of the comment
        comments_dict["Score"].append(comment.score)

        # Total number of replies
        comments_dict["Total replies"].append(len(comment.replies))

    all_comments = pd.DataFrame(comments_dict)
    return all_comments


comments(top_posts()['ID'][0])

# # PARSING
#
# top_posts_df = top_posts(duration='month')
#
# # printing the first few rows of the top posts DataFrame
# print("Top Posts: ")
# print(top_posts_df.head())
#
# # initializing comments_df as an empty DataFrame
# # comments_df = pd.DataFrame(columns=["ID", "Body", "Author", "Score", "Total replies"])
# comments_df = comments(top_posts()['ID'][0])
# # calling the comments function with the ID of a specific post to retrieve its comments
# post_id = 'your_post_id_here'
# try:
#     comments_df = comments(post_id)
#     print("\nComments:")
#     if not comments_df.empty:
#         comments_df = comments_df.append(comments_data, ignore_index=True)
#         print(comments_df.head())
#     else:
#         print("No comments found for the specified post!")
# except Exception as e:
#     print(f"An error occurred while fetching comments: {str(e)}")
#
# # printing the first few rows of the 'comments DataFrame'
# print("\nComments (without specific index):")
# print(comments_df.head())
#
# # Basic Statistics related to the dataframe
# print("Mean Score:", comments_df['Score'].mean())
# print("Median Total Replies:", comments_df['Total replies'].median())
# print("Total Comments:", len(comments_df))
#
# # filtering the comments with a score greater than 10
# high_score_comments = comments_df[comments_df['Score'] > 10]
#
# # sorting the comments in a descending order
# sorted_comments = comments_df.sort_values(by='Score', ascending=False)
#
# # grouping the comments by author and then calculating the mean score of each author
# author_scores = comments_df.groupby('Author')['Score'].mean()
#
# # printing the values
# print("Sorted Comments: ", sorted_comments)
# print("Author Scores: ", author_scores)
#
# # !pip install nltk
# import nltk
#
# nltk.download('punkt')  # downloading the missing resource
# from nltk.tokenize import word_tokenize
#
# # tokenizing the comment bodies
# comments_df['Tokenized Body'] = comments_df['Body'].apply(lambda x: word_tokenize(x))
#
# # visualization
# import matplotlib.pyplot as plt
#
# # creating a histogram of the comment scores
# plt.hist(comments_df['Score'], bins=20)
# plt.xlabel('Score')
# plt.ylabel('Frequency')
# plt.show()
#


import nltk

nltk.download('punkt')
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import string


def extract_keywords(text, num_keywords=10):
    # Tokenize the text into words
    words = word_tokenize(text)

    # Remove punctuation and convert to lower case
    words = [''.join(c for c in w if c not in string.punctuation) for w in words]
    words = [word.lower() for word in words if word]

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    # Count the frequency of each word
    word_freq = Counter(words)

    # Extract top num_keywords keywords
    keywords = word_freq.most_common(num_keywords)

    return keywords


# Get the top posts and comments and extract keywords from them
top_posts_df = top_posts('month')
comments_df = comments(top_posts_df['ID'][0])  # This gets the comments of the first post in top_posts_df

# Extracting Keywords from Post Text and Comment Body
top_posts_df['Keywords'] = top_posts_df['Post Text'].apply(extract_keywords)
comments_df['Keywords'] = comments_df['Body'].apply(extract_keywords)

print(top_posts_df[['Title', 'Keywords']])

print(comments_df[['Body', 'Keywords']])

list(top_posts_df[['Title', 'Keywords']].iloc[0])


# Define a function to create a new DataFrame for posts with the specified columns
def create_post_keywords_df(top_posts_df):
    post_keywords_df = pd.DataFrame()
    post_keywords_df['Date'] = top_posts_df.index
    post_keywords_df['Post ID'] = top_posts_df['ID']
    post_keywords_df['Score'] = top_posts_df['Score']
    post_keywords_df['Total Comments'] = top_posts_df['Total Comments']
    post_keywords_df['Keywords'] = top_posts_df['Post Text'].apply(extract_keywords)

    return post_keywords_df


top_posts_df = top_posts('month')
post_keywords_df = create_post_keywords_df(top_posts_df)

print(post_keywords_df.head())


# Define a function to create a new DataFrame for comments with the specified columns
def create_comment_keywords_df(comments_df):
    comment_keywords_df = pd.DataFrame()
    comment_keywords_df['Comment ID'] = comments_df['ID']
    comment_keywords_df['Score'] = comments_df['Score']
    comment_keywords_df['Total Replies'] = comments_df['Total replies']
    comment_keywords_df['Keywords'] = comments_df['Body'].apply(extract_keywords)

    return comment_keywords_df


# You will have to call comments() function for each post ID in top_posts_df and then create a DataFrame for each
# Here is an example for the first post in top_posts_df
comments_df = comments(top_posts_df['ID'][0])
comment_keywords_df = create_comment_keywords_df(comments_df)

print(comment_keywords_df.head())

from mysql_utils import create_connection, insert_post_metadata, insert_comment_metadata, \
    insert_keyword_get_id, execute_query, insert_into_junction_table, comment_id_exists

# insert into Posts table
connection = create_connection()

if connection.is_connected():
    # Insert into Posts table and get the IDs of the inserted rows
    for index, row in post_keywords_df.iterrows():
        post_id = insert_post_metadata(connection, row.to_dict())

        if post_id:
            # Insert into Keywords table and corresponding Junction tables
            for keyword in row['Keywords']:
                keyword_id = insert_keyword_get_id(connection, keyword)
                query = "INSERT INTO PostKeywords (PostID, KeywordID) VALUES (%s, %s)"
                execute_query(connection, query, (post_id, keyword_id))

    # Insert into Comments table and get the IDs of the inserted rows
    for index, row in comments_df.iterrows():
        comment_id = insert_comment_metadata(connection, row.to_dict())

        if comment_id:
            # Insert into CommentKeywords table
            for keyword in row['Keywords']:
                keyword_id = insert_keyword_get_id(connection, keyword)
                if keyword_id is not None:
                    insert_into_junction_table(connection, 'CommentKeywords', comment_id, keyword_id)





