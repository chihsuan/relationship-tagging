#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

'''
This module is to search keywords in move subtitle.

Define Keyword: keyword is name or term relationship.
ex: Jack, Dad

Intput: -> 1 realationship_file 2. subtitle_file
Output: keyword to time in subtitle and keyword_list 
        -> 1.search_result_csv_file 2. keyword_list
'''

import sys
import re
from collections import Counter

from modules import csv_io
from modules import time_format

OUTPUT_ROOT_PATH = 'output/'

def keyword_statistics(relationship_file, subtitle_file):
    
    relation_list = csv_io.read_csv(relationship_file)
    subtitle = read_subtitle_file(subtitle_file)

    relation_patterns = {}
    for relation in relation_list:
        relation_patterns[relation] = '[^(my)|^(your)|^(her)|^(his)|^(their)][\s]*' \
                                      + relation.lower() + "[^'\w]"
    
    subtitle_interval = []
    time_to_keyword = []
    keyword_list = []
    for line in subtitle:
        if line.strip():
            subtitle_interval.append(line)
            if len(subtitle_interval) < 2:
                continue

            if len(subtitle_interval) == 2:
                subtitle_time = line[:-2]
                continue
            
            time_to_keyword, keyword_list = keyword_matching(relation_patterns, line, subtitle_time,\
                                                             time_to_keyword, keyword_list)
        else:
            subtitle_interval=[]
            '''if keyword_number == MAX_KEYWORDS_IN_ONE_INTERVAL:
                for i in range(MAX_KEYWORDS_IN_ONE_INTERVAL):
                    time_to_keyword.pop()
            keyword_number=0'''
    
    frame_to_keyword = []
    for pair in time_to_keyword:
        start_frame, end_frame = time_format.to_frame(pair[0])
        new_pair = [start_frame, end_frame, pair[1]]
        frame_to_keyword.append(new_pair)

    csv_io.write_csv(OUTPUT_ROOT_PATH + 'statistics_result.csv', frame_to_keyword)
    csv_io.write_csv(OUTPUT_ROOT_PATH + 'keyword_list.csv', [keyword_list])


def keyword_matching(relation_patterns, line, subtitle_time, time_to_keyword, keyword_list):

    for relation in relation_patterns:
        if re.search(relation_patterns[relation], line.lower()):
            time_to_keyword.append([subtitle_time, relation])
            if relation not in keyword_list:
               keyword_list.append(relation) 
                
    return time_to_keyword, keyword_list

def read_subtitle_file(subtitle_file):

    with open(subtitle_file, 'r') as subtitle:
        subtitle = subtitle.readlines()
    return subtitle


if __name__=='__main__':
    if len(sys.argv) == 4:
        keyword_statistics(sys.argv[1], sys.argv[2])
    else:
        keyword_statistics('input/relationship.csv', 'input/movie.srt')
