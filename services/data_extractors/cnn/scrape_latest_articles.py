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

    urls_opened_in_current_batch = 0

    for rss_entry in rss_entries:
        try:
            webbrowser.open_new_tab(rss_entry.url)
            urls_opened_in_current_batch += 1

            if scrapes_per_batch == urls_opened_in_current_batch:
                time.sleep(ms_interval_between_batches / 1000)

            report['succeeded'] += 1

        except Exception as e:
            print(f'Exception has been raised : {str(e)}')
            report['failed'] += 1
