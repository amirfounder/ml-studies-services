import requests
from bs4 import BeautifulSoup

from daos import RssFeedUrl, RssEntrySource


source = next(iter(RssEntrySource.all(name='cnn')), None)
if not source:
    source = RssEntrySource(name='cnn')
    source.flush()


SOURCE_ID = source.id
RSS_PREFIX = 'http://rss.cnn.com/rss/cnn_'
RSS_PAGE_URL = 'https://www.cnn.com/services/rss/'


def get_topic_to_rss_url_map():
    try:
        response = requests.get(RSS_PAGE_URL)
        response.raise_for_status()

        markup = response.text
        soup = BeautifulSoup(markup, 'html.parser')

        a_tags = soup.select('table')[0].select('a')
        valid_urls = [a.text for a in a_tags if a.text.startswith(RSS_PREFIX)]

        for url in valid_urls:
            topic = url[len(RSS_PREFIX):].removesuffix('.rss')
            RssFeedUrl.get_or_create(name=topic, source_id=SOURCE_ID, url=url, return_list_if_one=False)

    except Exception as e:
        print(f'Exception occurred : {str(e)}')


if __name__ == '__main__':
    get_topic_to_rss_url_map()
