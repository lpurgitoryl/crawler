import praw
import pandas as pd
import json
import os
import pprint
import bs4
import requests
import re


def selected_subReddit():
    subreddit_name = input("\ninput just the subreddit name\n Ex. if you want \"r/MachineLearning\" only input \"MachineLearning\"\n")
    
    subreddit_name = selected_subRedditNameChecker(subreddit_name) # returns zero or reddit instance of type subreddit, use praw functions on this object
    if subreddit_name == 0:
        return 0;
    
    json_info = selected_subreddit_parameters(subreddit_name,600)
    # print(json_info)
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
    # limit = 1
    if limit >= 1000:
        limit = 999
    json_info = ""
    while user_input !=0:
        match user_input.upper():
            case 'HOT':
                for post in subreddit_name.hot(limit=limit):
                    links = parseLinks(post.selftext)
                    posts.append([post.title, post.score, post.id, post.url, post.num_comments, post.selftext, post.created, links])
                    df = pd.DataFrame(posts, columns=['title', 'score', 'id', 'url', 'num_comments', 'body', 'created', 'links'])
                    json_info = df.to_json(orient='records', indent=4)
                user_input = 0
            case 'NEW':
                for post in subreddit_name.new(limit=limit):
                    links = parseLinks(post.selftext)
                    posts.append([post.title, post.score, post.id, post.url, post.num_comments, post.selftext, post.created, links])
                    df = pd.DataFrame(posts, columns=['title', 'score', 'id', 'url', 'num_comments', 'body', 'created', 'links'])
                    json_info = df.to_json(orient='records', indent=4)
                user_input = 0

            case 'TOP':
                for post in subreddit_name.top(limit=limit):
                    links = parseLinks(post.selftext)
                    posts.append([post.title, post.score, post.id, post.url, post.num_comments, post.selftext, post.created, links])
                    df = pd.DataFrame(posts, columns=['title', 'score', 'id', 'url', 'num_comments', 'body', 'created', 'links'])
                    json_info = df.to_json(orient='records', indent=4)
                user_input = 0
            case 'RISING':
                for post in subreddit_name.rising(limit=limit):
                    links = parseLinks(post.selftext)
                    posts.append([post.title, post.score, post.id, post.url, post.num_comments, post.selftext, post.created, links])
                    df = pd.DataFrame(posts, columns=['title', 'score', 'id', 'url', 'num_comments', 'body', 'created', 'links'])
                    json_info = df.to_json(orient='records', indent=4)
                user_input = 0
            case "\n":
                for post in subreddit_name.top(limit=limit):
                    links = parseLinks(post.selftext)
                    posts.append([post.title, post.score, post.id, post.url, post.num_comments, post.selftext, post.created, links])
                    df = pd.DataFrame(posts, columns=['title', 'score', 'id', 'url', 'num_comments', 'body', 'created', 'links'])
                    json_info = df.to_json(orient='records', indent=4)
                user_input = 0
            case _:
                for post in subreddit_name.top(limit=limit):
                    links = parseLinks(post.selftext)
                    posts.append([post.title, post.score, post.id, post.url, post.num_comments, post.selftext, post.created, links])
                    df = pd.DataFrame(posts, columns=['title', 'score', 'id', 'url', 'num_comments', 'body', 'created', 'links'])
                    json_info = df.to_json(orient='records', indent=4)
                user_input = 0

    return json_info

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

def create_new_json_file(file_name):
    file_path = "crawled_data/" + file_name + ".json"
    if os.path.exists(file_path):
        print("File already exists.")
        return
    with open(file_path, "w") as outfile:
        outfile.write("[]")
        print("New JSON file created at", file_path)
def random_subreddits(): # find random subreddits based on params and add to file
    return '{"someKeyHere": "somePairHere}'
    

def enter_function_name_here():
    return '{"someKeyHere": "somePairHere}'

def making_dir_and_file(data="", file_num=0 ,flag=0, exit=0): # makes dir and file, checks if file size is less than 10mb

    if not os.path.exists('crawled_data'):
        os.makedirs('crawled_data')
        with open("crawled_data/user_search_"+ str(file_num) +".json", "w") as outfile:
            outfile.write('[')
            outfile.close()
    elif not os.path.exists("crawled_data/user_search_"+ str(file_num) +".json"):
        with open("crawled_data/user_search_"+ str(file_num) +".json", "w") as outfile:
            outfile.write('[')
            outfile.close()
            
    # TODO check for size, rn checks for delimiters
    # if flag != 0 and exit ==0 : # if zero needs deliminter
    temp = ''
    if flag !=0 and exit== 0:
        temp += '\n,' 
    flag = 1
    
    data = temp + data
    data_byte_size = len(data.encode('utf-8'))
    curr_file_size = os.stat("crawled_data/user_search_"+ str(file_num) +".json").st_size
    upper_byte_size_limit = 2000000 #2MB
    
    # check if data will make file go over limit.
    # if over limit, close curr file with ending bracket, increase file number, create new file add bracket
    if (  data_byte_size + curr_file_size ) > (upper_byte_size_limit) :
        with open("crawled_data/user_search_"+ str(file_num) +".json", "a") as outfile:
            data+="]"
            outfile.write(data)
            outfile.close()
        file_num +=1
        with open("crawled_data/user_search_"+ str(file_num) +".json", "w") as outfile:
            outfile.write('[')
            outfile.close()
        
    # append data to file
    with open("crawled_data/user_search_"+ str(file_num) +".json", "a") as outfile:
        # print("\nwriting this to file\n")
        # print(data)
        
        if exit ==1 :
            data+="]"
        outfile.write(data)
        outfile.close()

    # TODO: IF FILE SIZE REACHED LIMIT, INCREASE FILE NUM AND RUN LINES 89-98
    return flag,file_num
    
# TODO: FILE SIZE CHECKER, GENERATING THE RANDOM REDDITS AND SEARCHING THEM, SEARCHING REDDIT USERS, PARSING MARKDOWN
# Using the special variable 
# __name__
if __name__=="__main__":
    
    reddit = praw.Reddit(client_id="3IS_PPpIX3IkVIh-1f8cHQ",
    client_secret="AvAKHMywUgLyGlVSVD0bQMRpZbhb1w",
    user_agent ="crawler/scrapper")
    
    
    menu = '''\nHello, Welcome to r\'Crawler\n\nPlease select an NUMBER option\n\nEnter 1 to search for a specfic subredit\nEnter 2 to search for a reddit user\nEnter "exit" to terminate program\n'''
    init = input(menu)
    flag = 0 # zero when an extra ',' is not needed else if another option selected set to 1 to add delimiter
    file_num=0
    # the varible output is string in json format
    
    while init !=0:
        match init:
            case '1':
                output = selected_subReddit()
                print("\noutput\n")
                # print(output)
                if output != 0:
                      flag,file_num = making_dir_and_file(data=output, file_num=file_num,flag=flag)
                else: # error msg here
                    print("\n\nerror")
                init = input(menu)
            case '2':
                print("2")
                output =  random_subreddits()
                if output != 0:
                      flag,file_num = making_dir_and_file(output, file_num,flag)
                else: # error msg here
                    print("\n\n")
                init = input('\n\nPlease select an option\n')

            case '3':
                print("3")
                output = enter_function_name_here()
                if output != 0:
                      flag,file_num = making_dir_and_file(output, file_num,flag)
                else: # error msg here
                    print("\n\n")

                init = input('\n\nPlease select an option\n')
            
            case '4':
                print("4")
                output = enter_function_name_here()
                if output != 0:
                      flag,file_num = making_dir_and_file(output, file_num,flag)
                else: # error msg here
                    print("\n\n")

                init = input('\n\nPlease select an option\n')

            case '5':
                print("5")
                output = enter_function_name_here()
                if output != 0:
                      flag,file_num = making_dir_and_file(output, file_num,flag)
                else: # error msg here
                    print("\n\n")
                    
                init = input('\n\nPlease select an option\n')
            case 'exit':
                print("EXITING FILE")
                flag,file_num = making_dir_and_file(flag=flag, file_num=file_num,exit=1)
                print("Thank you for using rCrawler!")
                init = 0
            case _:
                print("default case statement")
                init = input('\nHello, Welcome to r\'Crawler\n\nPlease enter a valid number an option\n')