import praw
import pandas as pd
import json
import pprint



def selected_subReddit():
    subreddit_name = input("\ninput just the subreddit name\n Ex. if you want \"r/MachineLearning\" only input \"MachineLearning\"\n")
    
    subreddit_name = selected_subRedditNameChecker(subreddit_name) # returns zero or reddit instance of type subreddit
    if subreddit_name == 0:
        return 0;

    posts = []    
    for post in subreddit_name.hot(limit=10):
        posts.append([post.title, post.score, post.id, post.url, post.num_comments, post.selftext, post.created])
    df = pd.DataFrame(posts, columns=['title', 'score', 'id', 'url', 'num_comments', 'body', 'created'])
    json_info = df.to_json(orient='records', indent=4)
    return json_info[1:-1]

def selected_subRedditNameChecker(subreddit_name): #checks if user inputted name is valid... if not gives top three matches, returns 0 or reddit type of subredit
    checking_name = reddit.subreddits.search_by_name(subreddit_name)
    if subreddit_name != checking_name[0]:
        print("\nNo exact match found!\nDid you mean\n",checking_name[0]," or ", checking_name[1], " or ", checking_name[2], "\nPlease try again!!\n")
        return 0
    # print(type(checking_name[0]))
    return checking_name[0]

# Using the special variable 
# __name__
if __name__=="__main__":
    
    reddit = praw.Reddit(client_id="3IS_PPpIX3IkVIh-1f8cHQ",
    client_secret="AvAKHMywUgLyGlVSVD0bQMRpZbhb1w",
    user_agent ="crawler/scrapper")
    menu = '''\nHello, Welcome to r\'Crawler\n\nPlease select an NUMBER option\n\nEnter 1 to search for a subredit\nEnter 2 to search for a reddit user\nEnter 3 to search for a xyz\n'''
    init = input(menu)
    flag = 0 # zero when an extra ',' is not needed else if another option selected set to 1
    file = '['
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
                    
                init = input(menu)
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
            case '10':
                file +='\n]'
                print(file)
                with open("sample.json", "w") as outfile:
                    json.dump(json.loads(file), outfile, indent = 4)
                print("bye")
                init = 0
            case _:
                print("default case statement")
                init = input('\nHello, Welcome to r\'Crawler\n\nPlease enter a valid number an option\n')