from mongoengine import connect

from scrapers.pikore_scraper import pikore_content_scraper
from models.pikore_models import Instagram_Post


connect('pikore_data')
NUM_SCROLLS = 10

usernames = ['newbalance', 'nike', 'reebok']

for username in usernames:
    data = pikore_content_scraper(query=username, num_scrolls=NUM_SCROLLS, username=True)
    for result in data:
        Instagram_Post(username=result['username'],
                       likes=result['likes'],
                       comments=result['comments'],
                       description=result['description'],
                       time_posted=result['search_tag'],
                       hash_tags=result['hash_tags'],
                       extraction_time=result['extraction_time']).save()


tags = ['newbalance', 'nblove', 'nbfootball']

for tag in tags:
    data = pikore_content_scraper(query=tag, num_scrolls=NUM_SCROLLS, username=False)
    for result in data:
        Instagram_Post(username=result['username'],
                       likes=result['likes'],
                       comments=result['comments'],
                       description=result['description'],
                       time_posted=result['search_tag'],
                       hash_tags=result['hash_tags'],
                       extraction_time=result['extraction_time']).save()
