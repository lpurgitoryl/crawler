import praw
import pandas as pd
import json
import os
import re
import requests
import bs4

def selected_subReddit():
    subreddit_name = input("\ninput just the subreddit name\n Ex. if you want \"r/MachineLearning\" only input \"MachineLearning\"\n")
    
    subreddit_name = selected_subRedditNameChecker(subreddit_name) # returns zero or reddit instance of type subreddit, use praw functions on this object
    if subreddit_name == 0:
        return 0;
    
    json_info = selected_subreddit_parameters(subreddit_name,600)
    # print(json_info)
    # return json_info[1:-1]
    return json_info

def selected_subRedditNameChecker(subreddit_name): #checks if user inputted name is valid... if not gives top three matches, returns 0 or reddit type of subredit
    checking_name = reddit.subreddits.search_by_name(subreddit_name)
    if subreddit_name != checking_name[0]:
        print("\nNo exact match found!\nDid you mean\n",checking_name[0]," or ", checking_name[1], " or ", checking_name[2], "\nPlease try again!!\n")
        return 0
    # print(type(checking_name[0]))
    return checking_name[0]

def dumpJson(posts):
    data = []
    comments = []
    for post in posts:
        links = parseLinks(post.selftext)
        for comment in post.comments:
            try:
                comments.append(comment.body)
            except:
                comments.append("")
        data.append([post.title, post.score, post.id, post.url, post.num_comments, post.selftext, post.created, links, comments])
    df = pd.DataFrame(data, columns=['title', 'score', 'id', 'url', 'num_comments', 'body', 'created', 'links', 'comments'])
    return df.to_json(orient='records', indent=4)


def selected_subreddit_parameters(subreddit_name,limit): # returns comment forest , selects the catagory type to search ex. new, hot , rising, or top with limits... default will be NEW with a limit of _____
    # TODO Be able to assign a limit
    menu = "Please enter an option\n\nEnter NEW to search for NEW category\n\nEnter HOT to search for HOT category\n\nEnter TOP to search for TOP category\n\nEnter RISING to search for RISING category\nan invalid key will default...it will be top category with limit of 600\n"
    user_input = input(menu)
    # limit = 1
    if limit >= 1000:
        limit = 999
    json_info = ""
    while user_input !=0:
        match user_input.upper():
            case 'HOT':
                json_info = dumpJson(subreddit_name.hot(limit=limit))
                user_input = 0
            case 'NEW':
                json_info = dumpJson(subreddit_name.new(limit=limit))
                user_input = 0

            case 'TOP':
                json_info = dumpJson(subreddit_name.top(limit=limit))
                user_input = 0
            case 'RISING':
                json_info = dumpJson(subreddit_name.rising(limit=limit))
                user_input = 0
            case "\n":
                json_info = dumpJson(subreddit_name.top(limit=limit))
                user_input = 0
            case _:
                json_info = dumpJson(subreddit_name.top(limit=limit))
                user_input = 0

    return json_info

def random_subreddits(): # find random subreddits based on params and add to file
    return '{"someKeyHere": "somePairHere}'
    

def enter_function_name_here():
    return '{"someKeyHere": "somePairHere}'

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
            try:
                soup = bs4.BeautifulSoup(requests.get(link).content, 'html.parser')
                if soup.title is not None:
                    links.append({link : soup.title.string})
            except:
                pass

    return links
    

if __name__=="__main__":

    reddit = getCredential()

    
    menu = '''\nHello, Welcome to r\'Crawler\n\nPlease select an NUMBER option\n\nEnter 1 to search for a specfic subredit\nEnter "exit" to terminate program\n'''
    init = input(menu)
    flag = 0 # zero when an extra ',' is not needed else if another option selected set to 1 to add delimiter
    file_num=0
    # the varible output is string in json format
    
    while init !=0:
        match init:
            case '1':
                output = selected_subReddit()
            case '2':
                print("2")
                output =  random_subreddits()
            case '3':
                print("3")
                output = enter_function_name_here()
            
            case '4':
                print("4")
                output = enter_function_name_here()

            case '5':
                print("5")
                output = enter_function_name_here()
                
            case 'exit':
                print("EXITING FILE")
                print("Thank you for using rCrawler!")
                exit(0)
            case _:
                print("default case statement")
                init = input('\nHello, Welcome to r\'Crawler\n\nPlease enter a valid number an option\n')
        print("\noutput\n")
        with open("crawled_data/user_search_"+ str(file_num) +".json", "w") as outfile:
            outfile.write(output)
            outfile.close()
        init = input(menu)