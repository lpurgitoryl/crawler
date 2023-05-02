# DOCS
# https://praw.readthedocs.io/en/stable/getting_started/quick_start.html#submission-iteration
# https://praw.readthedocs.io/en/stable/tutorials/comments.html
# https://stackoverflow.com/questions/4041238/why-use-def-main
# https://towardsdatascience.com/scraping-reddit-data-1c0af3040768
import pandas as pd
import praw
from json import dumps, JSONEncoder

# To create a read-only Reddit instance, you need three pieces of information:
# Client ID
# Client secret
# User agent

reddit = praw.Reddit(client_id="3IS_PPpIX3IkVIh-1f8cHQ",
client_secret="AvAKHMywUgLyGlVSVD0bQMRpZbhb1w",
user_agent ="crawler/scrapper")


url = "https://www.reddit.com/r/funny/comments/3g1jfi/buttons/"
submission = reddit.submission(url=url)

# or with the submission’s ID which comes after comments/ in the URL:
# submission = reddit.submission("3g1jfi")


# submission.comments.replace_more(limit=0)
# for top_level_comment in submission.comments:
#     print(top_level_comment.body)

# get 10 hot posts from the MachineLearning subreddit
hot_posts = reddit.subreddit('MachineLearning').hot(limit=10)
for post in hot_posts:
    print(post.title)
    
# import pandas as pd
# posts = []
# ml_subreddit = reddit.subreddit('MachineLearning')
# for post in ml_subreddit.hot(limit=10):
#     posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
# posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
# print(posts)

# # assume you have a Subreddit instance bound to variable `subreddit`
# for submission in subreddit.hot(limit=10):
#     print(submission.title)
#     # Output: the submission's title
#     print(submission.score)
#     # Output: the submission's score
#     print(submission.id)
#     # Output: the submission's ID
#     print(submission.url)
#     # Output: the URL the submission points to or the submission's URL if it's a self post
