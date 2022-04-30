from datetime import datetime
from typing import Dict

import feedparser
from daos import (
    RssEntrySource as RssSource,
    RssEntryJsonFileIndexEntry as IndexEntry,
    RssEntryJsonFile as File
)

source = next(iter(RssSource.all(name='cnn')), None)
if not source:
    source = RssSource(name='cnn')
    source.flush()


SOURCE_ID = source.id


def sync_rss_entries(topic_to_rss_url_map: Dict[str, str]):
    topic_to_entries_map = {}
    for topic, url in topic_to_rss_url_map.items():

        try:
            entries = feedparser.parse(url).entries
            topic_to_entries_map[topic] = entries

        except Exception as e:
            print(f'Exception occurred : {str(e)}')

    for topic, rss_entries in topic_to_entries_map.items():

        try:
            latest_rss_entries = [rss_entry for rss_entry in rss_entries]
            latest_rss_entries_links = [e.get('link') for e in latest_rss_entries]

            already_synced_index_entries_links = [e.link for e in IndexEntry.all(link=latest_rss_entries_links)]

            not_synced_rss_entries = []
            for rss_entry in latest_rss_entries:
                if rss_entry.get('link') not in already_synced_index_entries_links:
                    not_synced_rss_entries.append(rss_entry)

            for rss_entry in not_synced_rss_entries:
                file = File()
                file.set_contents(rss_entry)
                file.flush()

                index_entry = IndexEntry()
                index_entry.file_path = file.path
                index_entry.source_id = SOURCE_ID
                index_entry.retrieved_at = datetime.now()
                index_entry.link = rss_entry.get('link')
                index_entry.flush()

        except Exception as e:
            print(f'Exception occurred : {str(e)}')
