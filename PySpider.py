from link_finder import LinkFinder
from controller import *
from urllib2 import urlopen
from domain import *


class PySpider:

    project_name = ''
    base_url     = ''
    domain_name  = ''
    queue_file   = ''
    crawled_file = ''
    queue        = set()
    crawled      = set()

    def __init__(self, attrs):
        PySpider.project_name = attrs['project_name']
        PySpider.base_url     = attrs['base_url']
        PySpider.domain_name  = attrs['domain_name']
        PySpider.queue_file   = PySpider.project_name + '/queue.txt'
        PySpider.crawled_file = PySpider.project_name + '/crawled.txt'
        if(attrs["flush"]):
            remove_data_files(PySpider.project_name, PySpider.base_url)
        PySpider.boot()
        PySpider.crawl_page('Initial spider', PySpider.base_url)

    @staticmethod
    def boot():
        create_project_directory(PySpider.project_name)
        create_data_files(PySpider.project_name, PySpider.base_url)
        PySpider.queue     = convert_file_to_set(PySpider.queue_file)
        PySpider.crawled   = convert_file_to_set(PySpider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in PySpider.crawled:
            print thread_name + " is crawling " + page_url
            print "Queue " + str(len(PySpider.queue)) + " | " + "Crawled " + str(len(PySpider.crawled))
            PySpider.add_links_to_queue(PySpider.gather_link(page_url))
            PySpider.queue.remove(page_url)
            PySpider.crawled.add(page_url)
            PySpider.update_files()


    @staticmethod
    def gather_link(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            # convert bytes from the python parsing data to human readable data
            if response.info()['Content-type']=='text/html' or \
                            response.info()['content-type'] == 'text/html; charset=utf-8' or \
                            response.info()['Content-type'] == 'text/html; charset=utf-8' or \
                            response.info()['Content-type'] == 'text/html; charset=UTF-8':
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(PySpider.base_url, page_url)
            finder.feed(html_string)
        except:
            print 'Error: can not crawl page'
            return set()
        return finder.page_links()

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if url in PySpider.queue or url in PySpider.crawled:
                continue
            if PySpider.domain_name not in get_sub_domain_name(url):
                continue
            PySpider.queue.add(url)

    @staticmethod
    def update_files():
        convert_set_to_file(PySpider.queue, PySpider.queue_file)
        convert_set_to_file(PySpider.crawled, PySpider.crawled_file)




