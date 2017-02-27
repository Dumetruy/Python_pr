"""Get numbers of words in each file from current folder """
import os
import sys


def get_files_list():
    """Get list of files from current folder"""
    file_name = sys.argv[0].split('/')[-1]
    file_list = os.listdir('.')
    file_list.remove(file_name)
    return file_list


def count_words(file_list):
    """Get numbers of words in each file"""

    count = 0

    for name_file in file_list:
        try:
            with open(name_file) as current_file:
                for line in current_file:
                    count += len(line.split())
        except IOError:
            pass

    return count


if __name__ == '__main__':
    FILES = get_files_list()
    print count_words(FILES)
