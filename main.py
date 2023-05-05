import praw
import pandas as pd
import os
import json
import pprint


    
# Using the special variable 
# __name__
if __name__=="__main__":
    
    if os.path.isfile('credentials.json'):
        with open('credentials.json') as f:
            data = json.load(f)
            client_id = data['client_id']
            client_secret = data['client_secret']
            user_agent = data['user_agent']
    else:
        client_id = input('Please enter your client_id: ')
        client_secret = input('Please enter your client_secret: ')
        user_agent = input('Please enter your user_agent: ')
        data = {}
        data['client_id'] = client_id
        data['client_secret'] = client_secret
        data['user_agent'] = user_agent
        with open('credentials.json', 'w') as outfile:
            json.dump(data, outfile)

    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
    
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