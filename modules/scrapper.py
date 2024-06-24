
import time, json, logging, datetime, os, pickle
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


from bs4 import BeautifulSoup
from tqdm import tqdm

from modules.helper import *

LOG_FILE = f'logs/{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.log'

if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(filename=LOG_FILE, encoding='utf-8', level=logging.DEBUG)
BASE_URL = 'https://www.instagram.com'

def get_posts_and_reels_from_profile(driver, profile_url, scrolls=5, delay=3):
    driver.get(profile_url)
    time.sleep(10)  # Allow initial page load

    posts_and_reels = set()  # Use a set to avoid duplicates

    for _ in range(scrolls):
        # Scroll down to load more posts
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(delay)  # Wait for new content to load

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all elements with href attributes
        elements = soup.find_all(href=True)

        # Extract URLs that start with '/p/' for posts and '/reel/' for reels
        hrefs_starting_with_p = [element['href'] for element in elements if element['href'].startswith('/p/')]
        hrefs_starting_with_reel = [element['href'] for element in elements if element['href'].startswith('/reel/')]

        # Add new links to the set
        posts_and_reels.update(hrefs_starting_with_p + hrefs_starting_with_reel)

    # Combine and format the URLs
    list_of_posts_and_reels = [BASE_URL + x for x in posts_and_reels]

    return list_of_posts_and_reels

def get_data_from_instagram():

    driver = login_in_instagram()

    # comments = scrap_comments_from_url(driver, 'https://www.instagram.com/p/C4RKBgCRAEk/')

    # Get the list of candidates

    with open('data/candidates.json', 'r') as f:
        candidates = json.load(f)

    # Get the list of posts from each candidate

    hFinal = []
        
    for candidate_profile in candidates:

        directory = f'data/{candidate_profile["name"]}'
        if not os.path.exists(directory):
            os.makedirs(directory)

        posts = get_posts_and_reels_from_profile(driver, candidate_profile["instagram_profile"])

        logging.info(f"Found {len(posts)} posts for {candidate_profile['name']}")

        for _ in tqdm(range(len(posts)), desc=f"Generating data for {candidate_profile['name']}", unit="post"):

            post = posts[_]
            post_link = post.split('/')[-2]

            if os.path.exists(f'{directory}/{post_link}.pkl'):
                logging.info(f"Reading logged post: {post_link}")
                with open(f'{directory}/{post_link}.pkl', 'rb') as f:
                    hRow = pickle.load(f)
                    hFinal.append(hRow)
                    logging.info(f"Appended post: {post_link}")
            
            else:
                logging.info(f"Scraping post: {post}")
                title, comments = scrap_comments_from_url(driver, post)

                hPost = []

                for comment in comments:

                    hRow = {
                        'candidate': candidate_profile['name'],
                        'post_url': post,
                        'post': title,
                        'comment': comment['comment'],
                        'likes': comment['likes'],
                        }

                    hPost.append(hRow)

                with open(f'{directory}/{post_link}.pkl', 'wb') as f:
                    pickle.dump(hPost, f)
                logging.info(f"Logged post: {post_link}")

                hFinal.append(hPost)
                logging.info(f"Appended post: {post_link}")

    driver.quit()

    return hFinal

def scrap_comments_from_url(driver, url, scrolls=5):

    driver.get(url)
    time.sleep(timer_load_page())  # Allow initial page load

    comment_data = []

    # XPath to the comments section

    xpath_express_base, xpath_title, rest_of_xpath_comment, rest_of_xpath_likes = getXPaths()

    title = driver.find_elements(By.XPATH, xpath_title)[0].text

    for i in range(scrolls):
        scroll_comments(driver)

    i = 1
    while True:
        try:
        
            comment = driver.find_elements(By.XPATH, xpath_express_base + str(i) + rest_of_xpath_comment)[0]
            likes = driver.find_elements(By.XPATH, xpath_express_base + str(i) + rest_of_xpath_likes)[0]

            if likes.text == 'Responder':
                likes_count = 0
            elif likes.text == 'Reply':
                likes_count = 0
            elif likes.text.endswith('curtida'):
                likes_count = int(likes.text.replace(' curtida', ''))
            elif likes.text.endswith('curtidas'):
                likes_count = int(likes.text.replace(' curtidas', '').replace('.', ''))
            elif likes.text.endswith(' like'):
                likes_count = int(likes.text.replace(' like', ''))
            elif likes.text.endswith(' likes'):
                likes_count = int(likes.text.replace(' likes', ''))
            else:
                likes_count = int(likes.text)

            logging.info('Comment ' + str(i) + ': ' + comment.text)
            logging.info('Likes: ' + str(likes_count))
            logging.info('---')

            comment_data.append({
                'comment': comment.text,
                'likes': likes_count
            })
            i += 1

        except IndexError as e:
            logging.info('End of comments')
            logging.info('scrapped ' + str(i) + ' comments')
            break

    return title, comment_data