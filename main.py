from queue import Queue
from threading import Thread
from time import time
from downloader import get_links, download_link, find_num_segments
import sys, os, shutil, subprocess
from env import OUTPUT_PATH, get_merged_file_path, MAX_THREADS

if len(sys.argv) != 3:
    print('Example input:$ python main.py media/535/1280x800')
    sys.exit(0)

# film_spec = 'media/523/1280x800'
film_spec = sys.argv[1]
segments = find_num_segments(film_spec)
film_name = sys.argv[2]

try:
    if not os.path.isdir(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
except:
    pass

def merge_files():
    list2 = list(map(lambda x: os.path.join(OUTPUT_PATH, x.split("/")[-1]), get_links(film_spec, segments)))
    with open(get_merged_file_path(film_name), 'wb') as merged:
        for ts_file in list2:
            with open(ts_file, 'rb') as mergefile:
                shutil.copyfileobj(mergefile, merged)


class DownloadWorker(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            link = self.queue.get()
            try:
                download_link(link)
            finally:
                print(link.split("/")[-1] + ' done')
                self.queue.task_done()


def main():
    ts = time()
    links = get_links(film_spec, segments)
    # Create a queue to communicate with the worker threads
    queue = Queue()
    # Create 8 worker threads
    for x in range(MAX_THREADS):
        worker = DownloadWorker(queue)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()
    # Put the tasks into the queue as a tuple
    for link in links:
        queue.put(link)
    # Causes the main thread to wait for the queue to finish processing all the tasks
    queue.join()

if __name__ == '__main__':
    main()
    merge_files()
    subprocess.run(['ffmpeg', '-i', get_merged_file_path(film_name, '.ts'),
                    get_merged_file_path(film_name, '.mp4')])
