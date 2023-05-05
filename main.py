import praw
import os
import json
import re
import requests
import bs4
import pandas as pd

def getCredential():
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
    return praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

def parseLinks(md):
    """ Return dict of links in markdown """
    INLINE_LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    FOOTNOTE_LINK_URL_RE = re.compile(r'\[(\d+)\]:\s+(\S+)')
    IS_LINK_RE = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    links = []

    for _, link in INLINE_LINK_RE.findall(md) + FOOTNOTE_LINK_URL_RE.findall(md):
        if IS_LINK_RE.match(link):
            links.append(link)

    return links


def crawlBySubreddit(subreddit_name):
    posts = []
    subreddit = reddit.subreddit(subreddit_name)
    for post in subreddit.hot(limit=10):
        # posts.append([post.title, post.score, post.id, post.url, post.num_comments, post.selftext, post.created, post.author, post.upvote_ratio, post.url])
        links = []
        for link in parseLinks(post.selftext):
            soup = bs4.BeautifulSoup(requests.get(link).content, 'html.parser')
            links.append({link : soup.title.string})
        posts.append([post.title, post.score, post.id, post.url, post.num_comments, post.selftext, post.created, post.author.id, post.author.name, links])
        # urls.append(post.upvote_ratio)
        # urls.append(post.url)
    #We also probably want author, upvote ratio, comments, and urls included in each post
    # df = pd.DataFrame(posts, columns=['title', 'score', 'id', 'url', 'num_comments', 'body', 'created', 'author'])
    df = pd.DataFrame(posts, columns=['title', 'score', 'id', 'url', 'num_comments', 'body', 'created', 'author_id', 'author_name', 'links'])
    json_info = df.to_json(orient='records', indent=4)
    print(json_info)
    
# Using the special variable 
# __name__
if __name__=="__main__":

    reddit = getCredential()
    
    init = input('\nHello, Welcome to r\'Crawler\n\nPlease select an NUMBER option\n TODO PUT MENU LIST HERE\n\n')
    tempList = []
    while init !=0:
        match init:
            case '1':
                subreddit_name = input("\ninput just the subreddit name\n Ex. if you want \"r/MachineLearning\" only input \"MachineLearning\"\n")
                crawlBySubreddit(subreddit_name)

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