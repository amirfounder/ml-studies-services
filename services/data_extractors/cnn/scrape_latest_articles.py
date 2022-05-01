import time
import warnings
import webbrowser

from daos import RssEntryIndexEntry as RssEntry


def scrape_latest_cnn_articles(**kwargs):
    warnings.warn("This function requires the Scraper server to be running and interacts with a browser.")
    report = {
        'succeeded': 0,
        'failed': 0
    }

    scrapes_per_batch = kwargs.get('scrapes_per_batch', 10)
    ms_interval_between_batches = kwargs.get('ms_interval_between_batches', 5 * 60 * 1000)

    rss_entries: list[RssEntry] = RssEntry.all(has_been_scraped=False)

    print(f'Rss Entries to scrape : {len(rss_entries)}')

    batches = [rss_entries[i:i + scrapes_per_batch] for i in range(0, len(rss_entries), scrapes_per_batch)]

    for batch in batches:
        for rss_entry in batch:
            try:
                webbrowser.open_new_tab(rss_entry.url)
                report['succeeded'] += 1

            except Exception as e:
                print(f'Exception has been raised : {str(e)}')
                report['failed'] += 1

        time.sleep(ms_interval_between_batches / 1000)
