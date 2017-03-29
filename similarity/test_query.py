#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: vasezhong
# @Date:   2017-03-28 20:06:27
# @Last Modified by:   vasezhong
# @Last Modified time: 2017-03-29 19:45:02

import os
import sys
import cv2

import util
import config
from extract_feature import CnnFeatureExtractor

header = """<style>
        .sim {
          border:solid;
          border-color:red;
        }
        </style>
        <script src="https://code.jquery.com/jquery-3.2.0.min.js"></script>
        <script src="https://fastcdn.org/FileSaver.js/1.1.20151003/FileSaver.min.js"></script>
        <script type="text/javascript">
          $(function(){
            $('td table img').click(function(){
              $(this).toggleClass("sim");
            });
            $('button').click(function(){
              content = ''
              $('img').each(function(){
                content = content + $(this).attr('src')
                if($(this).attr('class') != 'query') {
                  if($(this).attr('class') == 'sim') {
                    content = content + '\\t1';
                  } else {
                    content = content + '\\t0';
                  }
                }
                content = content + '\\n';
              })
              var file = new File([content], "label.txt", {type: "text/plain;charset=utf-8"});
              saveAs(file);
            });
          });
        </script>
        <button type="button">Export</button>"""
if __name__ == '__main__':
    if len(sys.argv) != 5:
        print 'Usage: python test_db.py [query_id2url] [query_folder] [db_id2url] [db_folder]'
        sys.exit(-1)

    query_id2url = {}
    query_id2url_file = sys.argv[1].strip()
    with open(query_id2url_file, 'r') as reader:
        lines = reader.readlines()
        for line in lines:
            segs = line.strip().split('\t')
            id = segs[0].strip()
            url = segs[1].strip()
            query_id2url[id] = url

    db_id2url = {}
    db_id2url_file = sys.argv[3].strip()
    with open(db_id2url_file, 'r') as reader:
        lines = reader.readlines()
        for line in lines:
            segs = lin.strip().split('\t')
            id = segs[0].strip()
            url = segs[1].strip()
            db_id2url[id] = url

    feature_extractor = CnnFeatureExtractor(config.alexnet_config)
    in_folder = sys.argv[2].strip()
    in_files = [in_file for in_file in os.listdir(in_folder)]
    in_binary_features = []
    for in_file in in_files:
        img_bgr = cv2.imread(os.path.join(in_folder, in_file))
        img_rgb = util.bgr2rgb(img_bgr)
        in_binary_features.append(feature_extractor.extract_binary_feature(img_rgb))
    assert len(in_files) == len(in_binary_features)
    print 'Totally', len(in_files), 'test images.'

    db_folder = sys.argv[4].strip()
    db_files = [db_file for db_file in os.listdir(db_folder)]
    db_binary_features = []
    for db_file in db_files:
        img_bgr = cv2.imread(os.path.join(db_folder, db_file))
        img_rgb = util.bgr2rgb(img_bgr)
        db_binary_features.append(feature_extractor.extract_binary_feature(img_rgb))
    assert len(db_files) == len(db_binary_features)
    print 'Totally', len(db_files), 'db images.'


    res = header + '\n<table>'
    for in_idx in range(len(in_files)):
        in_file, in_binary_feature = in_files[in_idx], in_binary_features[in_idx]
        assert in_file in query_id2url
        id2distance = {}
        for db_idx in range(len(db_files)):
            db_file, db_binary_feature = db_files[db_idx], db_binary_features[db_idx]
            distance = util.hamming_distance(in_binary_feature, db_binary_feature)
            id2distance[db_file] = distance

        sorted_id2distance = sorted(id2distance.items(), lambda x, y: cmp(x[1], y[1]))
        res += '<tr>'
        res += '<td valign="top"><img class="query" src="%s" width="300"/></td>' % query_id2url[in_file]
        res += '<td><table><tr><td>%s</td></table></td>' % '\n'.join(['<img src="%s" width="150"/>' % db_id2url[db_file] for (db_file, distance) in sorted_id2distance[:50]])
        res += '</tr>'
    res += '</table>'

    with open('result.html', 'w') as writer:
        writer.write(res)
