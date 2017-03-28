#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: vasezhong
# @Date:   2017-03-28 19:54:56
# @Last Modified by:   vasezhong
# @Last Modified time: 2017-03-28 20:03:06


alexnet_config = {
    'gpu_id': 0,
    'batch_size': 1,
    'channel_num': 3,
    'img_height': 227,
    'img_width': 227,
    'raw_scale': 255,
    'input_scale': 1,
    'feature_layer_name': 'fc7',
    'binary_feature_layer_name': 'fc8_kevin_encode',
    'binary_threshold': 0.5,
    'mean_file': '../model/bvlc_alexnet/',
    'model_def': r'../model/.prototxt',
    'model_weights': r'../model/.caffemodel'
}

vgg19_config = {
    'gpu_id': 0,
    'batch_size': 1,
    'channel_num': 3,
    'img_height': 224,
    'img_width': 224,
    'raw_scale': 255,
    'input_scale': 1,
    'feature_layer_name': 'fc7',
    'mean_file': '../model/bvlc_alexnet/',
    'model_def': r'../model/.prototxt',
    'model_weights': r'../model/.caffemodel'
}