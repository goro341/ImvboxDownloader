OUTPUT_PATH = '/Users/masoudjaveri/Desktop/output'
MAX_THREADS = 40
import os
def get_merged_file_path(file_name, format):
    return os.path.join('/Users/masoudjaveri/Desktop', file_name + format)
