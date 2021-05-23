import os, argparse, codecs, time, re
from progress.bar import Bar
from multiprocessing.pool import ThreadPool as Pool
from datetime import datetime
from itertools import product

#found_items = []

def file_ops(path):
    #file_count = 0
    path_files = []
    for root, _, fnames in os.walk(path):
        #files = [f for f in files if not f[0] == '.']
        files = []
        for f in fnames:
            if not f[0] == '.':
                files.append(f)
                path_files.append(os.path.join(root, f))
                #file_count += 1
    
    return path_files


def grep_worker2(filepath, search_param):
    found_items = []
    with codecs.open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if search_param in line:
                found_items.append(line)
                print(line, end='')
    return found_items


def grep_worker(filepaths, search_param):
    #global found_items
    found_items = []

    for filepath in filepaths:
        with codecs.open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            found_items.extend(list(filter(lambda x:search_param, lines)))
    return found_items


def convert(seconds): 
    min, sec = divmod(seconds, 60) 
    hour, min = divmod(min, 60) 
    return "%d:%02d:%02d" % (hour, min, sec)


def get_chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def main():
        # last three arguments are optional
        # bp @tesla.com tesla.txt /path/data 100 200
        parser = argparse.ArgumentParser()
        parser.add_argument('domain', help="Domain to search")
        parser.add_argument('output', help="Output file name")
        parser.add_argument('-d', '--data', type=str, nargs='?', default="/opt/breach-parse/BreachCompilation/data", help="Data to parse")
        parser.add_argument('-l', '--limit-size', type=int, nargs='?', const=50, help="File size limit in MB")
        parser.add_argument('-t', '--thread-size', type=int, nargs='?', const=50, help="Thread size")
        args = parser.parse_args()

        print(args.data)
        print(args.thread_size)
        print(len(file_ops(args.data)))

        fpaths = file_ops(args.data)
        chunks = get_chunks(fpaths, 100)

        print("Time started: {}".format((datetime.now())))
        start = time.time()
        pool = Pool(args.thread_size)
        # bar = Bar('Progress:', max=len(fpaths))
        # for dFile in fpaths:
        #     bar.next()
        #     pool.apply_async(grep_worker, (dFile, args.domain,))
            #grep_worker(dFile, args.domain)
        
        for a_chunk in chunks:
            result = pool.apply(grep_worker, (list(a_chunk), args.domain,))
            print(result)

        # with Pool(args.thread_size) as pool:
        #     pool.starmap(grep_worker, product(fpaths, args.domain))

        # pool.join()
        # pool.close()
        
        end = time.time()
        print("\nTime Elapsed: {}".format(convert(end - start)))
 
 
if __name__ == '__main__':
          main()