# Project name
import os

# Generate the project folder. Each website you crawl is a separate project (folder)
def create_project_directory(directory):
    if not os.path.exists(directory):                           # check if it exsits
        print "Creating the project " + directory
        os.mkdir(directory)
    else:
        print "The project " + directory + " has already been created. "

def remove_data_files(project_name):
    queue = project_name + '/queue.txt'
    crawled = project_name + '/crawled.txt'
    if os.path.isfile(queue):
        os.remove(queue)
    if os.path.isfile(crawled):
        os.remove(crawled)


# Create a queue to store the crawled files, and a queue to store the files to be crawled.
def create_data_files(project_name, base_url):
    queue   = project_name + '/queue.txt'
    crawled = project_name + '/crawled.txt'

    if not os.path.exists(queue):
        print "Creating the queue file of " + queue
        f = open(queue,'w')
        f.write(base_url)
        f.close()
    if not os.path.exists(crawled):
        print "Creating the crawled file of " + crawled
        f = open(crawled,'w')
        f.write('')
        f.close()

def write_file(path, item):
    f = open(path, 'w')
    f.write(path)
    f.close()

def offer_to_queue(path, item):
    with open(path, 'a') as file:
        file.write(item + '\n')

def delete_all_from_queue(path):
    with open(path, 'w'):
        pass

def convert_file_to_set(path):
    curSet = set()
    with open(path, 'rt') as f:
        for line in f:
            curSet.add(line.replace('\n', ''))

    return curSet

def convert_set_to_file(links, file):
    delete_all_from_queue(file)
    for link in sorted(links):
        offer_to_queue(file, link)