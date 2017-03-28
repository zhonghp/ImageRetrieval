#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: vasezhong
# @Date:   2017-03-28 20:06:27
# @Last Modified by:   vasezhong
# @Last Modified time: 2017-03-28 20:18:59

import os
import sys
import cv2

import util
import config
from extract_feature import CnnFeatureExtractor


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: python test_db.py [db_folder] [in_folder]'
        sys.exit(-1)

    feature_extractor = CnnFeatureExtractor(config.alexnet_config)
    db_folder = sys.argv[1].strip()
    db_files = [db_file for db_file in os.listdir(db_folder)]
    db_binary_features = []
    for db_file in db_files:
        img_bgr = cv2.imread(os.path.join(db_folder, db_file))
        img_rgb = util.bgr2rgb(img_bgr)
        db_binary_features.append(feature_extractor.extract_binary_feature(img_rgb))
    assert len(db_files) == len(db_binary_features)
    print 'Totally', len(db_files), 'db images.'

    in_folder = sys.argv[1].strip()
    in_files = [in_file for in_file in os.listdir(in_folder)]
    in_binary_features = []
    for in_file in in_files:
        img_bgr = cv2.imread(os.path.join(in_folder, in_file))
        img_rgb = util.bgr2rgb(img_bgr)
        in_binary_features.append(feature_extractor.extract_binary_feature(img_rgb))
    assert len(in_files) == len(in_binary_features)
    print 'Totally', len(in_files), 'test images.'

    id2distance = {}
    for in_idx in range(len(in_files)):
        in_file, in_binary_feature = in_files[in_idx], in_binary_features[in_idx]
        min_distance = 256
        for db_idx in range(len(db_files)):
            db_file, db_binary_feature = db_files[db_idx], db_binary_features[db_idx]
            distance = util.hamming_distance(in_binary_feature, db_binary_feature)
            if distance < min_distance:
                min_distance = distance
        assert in_file not in id2distance
        id2distance[in_file] = min_distance

