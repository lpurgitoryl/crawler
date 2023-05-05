import praw
import pandas as pd
import json
import os
import pprint



def selected_subReddit():
    subreddit_name = input("\ninput just the subreddit name\n Ex. if you want \"r/MachineLearning\" only input \"MachineLearning\"\n")
    
    subreddit_name = selected_subRedditNameChecker(subreddit_name) # returns zero or reddit instance of type subreddit, use praw functions on this object
    if subreddit_name == 0:
        return 0;
    
    json_info = selected_subreddit_parameters(subreddit_name,600)
    
    return json_info[1:-1]

def selected_subRedditNameChecker(subreddit_name): #checks if user inputted name is valid... if not gives top three matches, returns 0 or reddit type of subredit
    checking_name = reddit.subreddits.search_by_name(subreddit_name)
    if subreddit_name != checking_name[0]:
        print("\nNo exact match found!\nDid you mean\n",checking_name[0]," or ", checking_name[1], " or ", checking_name[2], "\nPlease try again!!\n")
        return 0
    # print(type(checking_name[0]))
    return checking_name[0]

def selected_subreddit_parameters(subreddit_name,limit): # returns comment forest , selects the catagory type to search ex. new, hot , rising, or top with limits... default will be NEW with a limit of _____
    posts = []
    # TODO Be able to assign a limit
    menu = "Please enter an option\n\nEnter NEW to search for NEW catagory\n\nEnter HOT to search for HOT catagory\n\nEnter TOP to search for TOP catagory\n\nEnter RISING to search for RISING catagory\nan invalid key will default...it will be top catagory with limit of 600\n"
    user_input = input(menu)
    if limit >= 1000:
        limit = 999
    json = ""
    while user_input !=0:
        match user_input.upper():
            case 'HOT':
                for post in subreddit_name.hot(limit=limit):
                    posts.append([post.title, post.score, post.id, post.url, post.num_comments, post.selftext, post.created])
                    df = pd.DataFrame(posts, columns=['title', 'score', 'id', 'url', 'num_comments', 'body', 'created'])
                    json = df.to_json(orient='records', indent=4)
                user_input = 0
            case 'NEW':
                for post in subreddit_name.new(limit=limit):
                    posts.append([post.title, post.score, post.id, post.url, post.num_comments, post.selftext, post.created])
                    df = pd.DataFrame(posts, columns=['title', 'score', 'id', 'url', 'num_comments', 'body', 'created'])
                    json = df.to_json(orient='records', indent=4)
                user_input = 0

            case 'TOP':
                for post in subreddit_name.top(limit=limit):
                    posts.append([post.title, post.score, post.id, post.url, post.num_comments, post.selftext, post.created])
                    df = pd.DataFrame(posts, columns=['title', 'score', 'id', 'url', 'num_comments', 'body', 'created'])
                    json = df.to_json(orient='records', indent=4)
                user_input = 0
            case 'RISING':
                for post in subreddit_name.rising(limit=limit):
                    posts.append([post.title, post.score, post.id, post.url, post.num_comments, post.selftext, post.created])
                    df = pd.DataFrame(posts, columns=['title', 'score', 'id', 'url', 'num_comments', 'body', 'created'])
                    json = df.to_json(orient='records', indent=4)
                user_input = 0
            case "\n":
                for post in subreddit_name.top(limit=limit):
                    posts.append([post.title, post.score, post.id, post.url, post.num_comments, post.selftext, post.created])
                    df = pd.DataFrame(posts, columns=['title', 'score', 'id', 'url', 'num_comments', 'body', 'created'])
                    json = df.to_json(orient='records', indent=4)
                user_input = 0
            case _:
                for post in subreddit_name.top(limit=limit):
                    posts.append([post.title, post.score, post.id, post.url, post.num_comments, post.selftext, post.created])
                    df = pd.DataFrame(posts, columns=['title', 'score', 'id', 'url', 'num_comments', 'body', 'created'])
                    json = df.to_json(orient='records', indent=4)
                user_input = 0

    return json
    

def random_subreddits(): # find random subreddits based on params and add to file
    return '{"someKeyHere": "somePairHere}'
    

def enter_function_name_here():
    return '{"someKeyHere": "somePairHere}'

# Using the special variable 
# __name__
if __name__=="__main__":
    
    reddit = praw.Reddit(client_id="3IS_PPpIX3IkVIh-1f8cHQ",
    client_secret="AvAKHMywUgLyGlVSVD0bQMRpZbhb1w",
    user_agent ="crawler/scrapper")
    menu = '''\nHello, Welcome to r\'Crawler\n\nPlease select an NUMBER option\n\nEnter 1 to search for a specfic subredit\nEnter 2 to search for a reddit user\nEnter 3 to search for a xyz\n'''
    init = input(menu)
    flag = 0 # zero when an extra ',' is not needed else if another option selected set to 1 to add delimiter
    file = '['
    # the varible output is string in json format
    
    while init !=0:
        match init:
            case '1':
                output = selected_subReddit()
                if output != 0:  
                    print(output)
                    if flag != 0:
                        file +='\n,'
                    file += output
                    flag = 1
                else: # error msg here
                    print("\n\n")
                init = input(menu)
            case '2':
                print("2")
                output =  random_subreddits()
                if output != 0:  
                    print(output)
                    if flag != 0:
                        file +='\n,'
                    file += output
                    flag = 1
                init = input('\n\nPlease select an option\n')

            case '3':
                print("3")
                output = enter_function_name_here()
                if output != 0:  
                    print(output)
                    if flag != 0:
                        file +='\n,'
                    file += output
                    flag = 1
                init = input('\n\nPlease select an option\n')
            
            case '4':
                print("4")
                output = enter_function_name_here()
                if output != 0:  
                    print(output)
                    if flag != 0:
                        file +='\n,'
                    file += output
                    flag = 1
                init = input('\n\nPlease select an option\n')

            case '5':
                print("5")
                output = enter_function_name_here()
                if output != 0:  
                    print(output)
                    if flag != 0:
                        file +='\n,'
                    file += output
                    flag = 1
                init = input('\n\nPlease select an option\n')
            case '10':
                print("EXITING FILE")
                file +='\n]'
                # print(file)
                with open("sample.json", "w") as outfile:
                    json.dump(json.loads(file), outfile, indent = 4)
                print("bye")
                init = 0
            case _:
                print("default case statement")
                init = input('\nHello, Welcome to r\'Crawler\n\nPlease enter a valid number an option\n')