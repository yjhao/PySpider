import threading
import argparse
from Queue import Queue
from PySpider import PySpider
from domain import *
from controller import *


parser = argparse.ArgumentParser(description="Multi-threaded website crawler written in Python")

parser.add_argument("--flush", help="empty project folder prior to crawling", action="store_true")

args = parser.parse_args()

PROJECT_NAME = 'cs326'
HOMEPAGE = 'http://umass-cs-326.github.io/'
DOMAIN_NAME = get_sub_domain_name(HOMEPAGE)

QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()

attrs = {
    'project_name': PROJECT_NAME,
    'base_url': HOMEPAGE,
    'domain_name': DOMAIN_NAME,
    'flush': args.flush
}

PySpider(attrs)


# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        PySpider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in convert_file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = convert_file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()

create_workers()
crawl()