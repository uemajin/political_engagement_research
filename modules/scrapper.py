from modules.helper import *

from bs4 import BeautifulSoup

import json

BASE_URL = 'https://www.instagram.com'

def get_posts_from_profile(driver, profile_url):
    
        driver.get(profile_url)
        time.sleep(10)
    
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        elements = soup.find_all(class_="x1i10hfl", href=True)

        hrefs_starting_with_p = [element['href'] for element in elements if element['href'].startswith('/p/')]

        list_of_posts = [BASE_URL + x for x in hrefs_starting_with_p]

        return list_of_posts

def get_data_from_instagram():

    driver = login_in_instagram()

    # comments = scrap_comments_from_url(driver, 'https://www.instagram.com/p/C4RKBgCRAEk/')

    # Get the list of candidates

    with open('data/candidates.json', 'r') as f:
        candidates = json.load(f)

    # Get the list of posts from each candidate
        
    for candidate_profile in candidates:
        posts = get_posts_from_profile(driver, candidate_profile["instagram_profile"])

        candidate_profile['comments'] = []

        for post in posts:

            candidate_profile['comments'] += scrap_comments_from_url(driver, post)

    driver.quit()

    return candidates

    
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