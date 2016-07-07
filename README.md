# PySpider
This is an open source, multi-threaded website crawler written in Python utilizing various modules and APIs.

Specify the website that needs to be crawled in the main.py.

***

The analytics, data harvesting, and search algorithms are being developed.


***

## Python queue

Use queue to implement a thread safe task queue. Each task is a URL link that needs to be crawled.

### queue.get()

Each time, a worker gets the first item in the queue, and run the spyder.

### queue.put()
When a worker's spyder has finished, the next level (BFS) url are transferred to a set, and ```queue.put(url)```.


### queue.join
Using ```queue.join()``` to ensure thread safe between thread get. 

"The count goes down whenever a consumer thread calls ```task_done()``` to indicate that the item was retrieved and all work on it is complete. When the count of unfinished tasks drops to zero, ```join() ```unblocks."


## Eliminate conflication between threads
It is possible that thread A add URl u1, u2, u3 in the to-be-crawled file because u1, u2, u3 do not exist in the hashset. 

In the meantime, another thread B could possibily add URl u1, u2, u3 as well, because they do not exist in the hashset AT THE SAME TIME WHEN Thread A is performed. (Hashset is not threading safe)

u1, u2, u3 are all added and wrote to a file.

In order to solve this issue that do not crawl a url repetitively. When adding the URL to the queue, transfer them to a set first.

### Improvement
In the future, a **lock** mechanism will be implemented in order to resolve this issue. Add a lock to the hashset, and use ```lock.acquire()``` and ```lock.release()```


