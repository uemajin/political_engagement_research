from modules.helper import *

from bs4 import BeautifulSoup

import json

def get_data_from_instagram():

    driver = login_in_instagram()

    comments = scrap_comments_from_url(driver, 'https://www.instagram.com/p/C4RKBgCRAEk/')

    # Get the list of candidates
    
    ''''
    TBD: List all the posts from each candidate function
    '''

    # Get the list of posts from each candidate

    driver.quit()

    return comments

    
def scrap_comments_from_url(driver, url):

    driver.get(url)
    time.sleep(10)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    script_tag = soup.find_all('script', type='application/json') #Script tag contains comments

    list_of_comments = []

    for comment_tag in script_tag:

        json_string = comment_tag.string

        try:
            # Attempt to parse the JSON string
            data = json.loads(json_string)
            # Now 'data' contains the parsed JSON object
            
            array_of_comments = data['require'][0][3][0]['__bbox']['require'][0][3][1]['__bbox']['result']['data']['xdt_api__v1__media__media_id__comments__connection']['edges']

            for comment in array_of_comments:

                hComment = {
                    'comment' : comment['node']['text'].replace('\n', ''),
                    'likes' : comment['node']['comment_like_count']
                }

                list_of_comments.append(hComment)

        except json.JSONDecodeError as e:
            # If the JSON string is invalid, print an error message
            #print("Error parsing JSON:", e)
            pass

        except KeyError as e:
            #print("Couldn't find key for dict:", e)
            pass

        except TypeError as e:
            #print("Couldn't find the correct format:", e)
            pass

        except IndexError as e:
        #print("Not the right format:", e)
            pass

    return list_of_comments