import praw
import pandas as pd
import json
import pprint


    
# Using the special variable 
# __name__
if __name__=="__main__":
    
    reddit = praw.Reddit(client_id="3IS_PPpIX3IkVIh-1f8cHQ",
    client_secret="AvAKHMywUgLyGlVSVD0bQMRpZbhb1w",
    user_agent ="crawler/scrapper")
    
    init = input('\nHello, Welcome to r\'Crawler\n\nPlease select an NUMBER option\n TODO PUT MENU LIST HERE\n\n')
    tempList = []
    while init !=0:
        match init:
            case '1':
                subreddit_name = input("\ninput just the subreddit name\n Ex. if you want \"r/MachineLearning\" only input \"MachineLearning\"\n")
                posts = []
                subreddit = reddit.subreddit(subreddit_name)
                for post in subreddit.hot(limit=10):
                    posts.append([post.title, post.score, post.id, post.url, post.num_comments, post.selftext, post.created])
                df = pd.DataFrame(posts, columns=['title', 'score', 'id', 'url', 'num_comments', 'body', 'created'])
                json_info = df.to_json(orient='records', indent=4)
                print(json_info)

            case '2':
                print("2")
                init = input('\n\nPlease select an option\n')

            case '3':
                print("3")
                init = input('\n\nPlease select an option\n')
            
            case '4':
                print("4")
                init = input('\n\nPlease select an option\n')

            case '5':
                print("5")
                init = input('\n\nPlease select an option\n')
            case _:
                print("default case statement")
                init = input('\nHello, Welcome to r\'Crawler\n\nPlease select an option\n')