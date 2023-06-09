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
    return json_info[1:-1]

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