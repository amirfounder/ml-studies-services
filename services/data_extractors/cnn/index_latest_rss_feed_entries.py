from datetime import datetime

import feedparser
from daos import (
    RssEntrySource as RssSource,
    RssEntryIndexEntry as IndexEntry,
    RssEntryJsonFile as File,
    RssFeedUrl as FeedUrl
)

source = next(iter(RssSource.all(name='cnn')), None)
if not source:
    source = RssSource(name='cnn')
    source.flush()


SOURCE_ID = source.id


def index_latest_cnn_rss_feed_entries():
    report = {'new_entries_synced': {}}

    cnn_source = RssSource.get_or_create(name='cnn', return_list_if_one=False)
    feed_urls = FeedUrl.all(source_id=cnn_source.id)

    topic_to_url_map = {feed_url.name: feed_url.url for feed_url in feed_urls}
    topic_to_entries_map = {topic: feedparser.parse(url).entries for topic, url in topic_to_url_map.items()}

    for topic, rss_entries in topic_to_entries_map.items():

        try:
            latest_rss_entries = []
            for rss_entry in rss_entries:
                rss_entry['link'] = rss_entry.get('link').split('?')[0]
                if 'cnn.com' not in rss_entry.get('link'):
                    continue
                latest_rss_entries.append(rss_entry)
            latest_rss_entries_urls = [e.get('link') for e in latest_rss_entries]

            already_synced_index_entries_urls = [e.url for e in IndexEntry.all(url=latest_rss_entries_urls)]

            not_synced_rss_entries = []
            for rss_entry in latest_rss_entries:
                if rss_entry.get('link') not in already_synced_index_entries_urls:
                    not_synced_rss_entries.append(rss_entry)

            for rss_entry in not_synced_rss_entries:
                file = File()
                file.set_contents(rss_entry)
                file.flush()

                index_entry = IndexEntry()
                index_entry.file_path = file.path
                index_entry.source_id = SOURCE_ID
                index_entry.retrieved_at = datetime.now()
                index_entry.url = rss_entry.get('link')
                index_entry.flush()

            report['new_entries_synced'][topic] = len(not_synced_rss_entries)

        except Exception as e:
            print(f'Exception occurred : {str(e)}')

    return report
