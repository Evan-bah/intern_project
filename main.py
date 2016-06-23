from mongoengine import connect

from scrapers.pikore_scraper import pikore_tag_scraper
from models.pikore_models import Instagram_Post


connect('pikore_data')

tag_data = pikore_tag_scraper('newbalance', 1)


for tag in tag_data:
    Instagram_Post(username=tag['username'],
                   likes=tag['likes'],
                   comments=tag['comments'],
                   description=tag['description'],
                   search_tag=tag['search_tag']).save()
