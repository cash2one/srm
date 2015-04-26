#!/usr/bin/python
# -*- coding: utf-8 -*-

import os.path
from datetime import datetime
from rank_params import PARAMS

__all__ = ['get_html_folder_path', 'create_html_folder', 'create_subfolder', 'add_page', 'add_search_query']

html_folder = None


def get_html_folder_path():
    global html_folder
    return html_folder


def create_html_folder():
    if not PARAMS['SAVE_GOOGLE_OUTPUT']:
        return
    root = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    global html_folder
    fld_name = datetime.now().strftime('%y%m%d_%H%M%S')
    html_folder = os.path.join(root, 'google_output', fld_name).replace('\\', '/')
    os.makedirs(html_folder)


def create_subfolder(subfolder_name):
    if not PARAMS['SAVE_GOOGLE_OUTPUT']:
        return
    subfolder = os.path.join(html_folder, subfolder_name.strip()).replace('\\', '/')
    os.makedirs(subfolder)


def add_page(subfolder_name, page_num, page_contents):
    if not PARAMS['SAVE_GOOGLE_OUTPUT']:
        return
    file_name = '%02d.html' % page_num
    full_file_name = os.path.join(html_folder, subfolder_name.strip(), file_name).replace('\\', '/')
    with open(full_file_name, 'w') as f:
        f.write(page_contents)


def add_search_query(subfolder_name, page_num, squery):
    if not PARAMS['SAVE_GOOGLE_OUTPUT']:
        return
    file_name = 'search_query.txt'
    full_file_name = os.path.join(html_folder, subfolder_name.strip(), file_name).replace('\\', '/')
    with open(full_file_name, 'a') as f:
        f.write(str(page_num) + ': ' + squery + '\n')

# if __name__ == '__main__':
#     create_html_folder()
#     subfolder = 'Arl make do'
#     create_subfolder(subfolder)
#     add_page(subfolder,0, 'yyyyyyyyyyyyyyyyyyy uuuuuuuuuuu')
#     add_search_query(subfolder, 1, 'llllllllllllllllll')
#     add_search_query(subfolder, 2, 'llllllllllllllllll')