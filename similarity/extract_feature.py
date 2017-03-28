#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: vasezhong
# @Date:   2017-03-28 19:30:09
# @Last Modified by:   vasezhong
# @Last Modified time: 2017-03-28 20:34:14

import caffe
import skimage
import numpy as np

class FeatureExtractor:
    def __init__(self, config_dict):
        self.config = config_dict

    def extract_feature(self, img_rgb):
        pass

    def extract_binary_feature(self, img_rgb):
        pass


class CnnFeatureExtractor(FeatureExtractor):
    def __init__(self, config_dict):
        FeatureExtractor.__init__(config_dict)

        if self.config['gpu_id'] < 0:
            caffe.set_mode_cpu()
        else:
            caffe.set_device(self.config['gpu_id'])
            caffe.set_mode_gpu()

        self.__net = caffe.Net(self.config['model_def'], self.config['model_weights'], caffe.TEST)
        self.__transformer = caffe.io.Transformer({'data': self.__net.blobs['data'].data.shape})
        self.__transformer.set_transpose('data', (2, 0, 1))
        self.__transformer.set_raw_scale('data', self.config['raw_scale'])
        if 'mean_file' in self.config and self.config['mean_file'] != '':
            mu = np.load(self.config['mean_file'])
            mu = mu.mean(1).mean(1)
            self.__transformer.set_mean('data', mu)
        self.__transformer.set_input_scale('data', self.config['input_scale'])
        self.__transformer.set_channel_swap('data', (2, 1, 0))  # swap channel from RGB to BGR
        self.__net.blobs['data'].reshape(self.config['batch_size'], self.config['channel_num'], self.config['img_height'], self.config['img_width'])

    def forward(self, img_rgb):
        img_rgb = skimage.img_as_float(img_rgb).astype(np.float32)
        transformed_img = self.__transformer.preprocess('data', img_rgb)
        self.__net.blobs['data'].data[...] = transformed_img
        self.__net.forward()

    def extract_feature(self, img_rgb):
        self.forward(img_rgb)
        feature = self.__net.blobs[self.config['feature_layer_name']].data[0]
        return feature.copy()

    def extract_binary_feature(self, img_rgb):
        self.forward(img_rgb)
        binary_feature = self.__net.blobs[self.config['binary_feature_layer_name']].data[0]
        return binary_feature.copy() > self.config['binary_threshold']


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print 'Usage: python extract_feature.py [img_file1] [img_file2]'
        sys.exit(-1)

    import cv2
    import util
    import config
    extractor = FeatureExtractor(config.alexnet_config)

    img_file1 = sys.argv[1].strip()
    img_file2 = sys.argv[2].strip()

    img_bgr1 = cv2.imread(img_file1)
    img_bgr2 = cv2.imread(img_file2)
    img_rgb1 = util.bgr2rgb(img_bgr1)
    img_rgb2 = util.bgr2rgb(img_bgr2)
    binary_feature1 = extractor.extract_binary_feature(img_rgb1)
    binary_feature2 = extractor.extract_binary_feature(img_rgb2)
    print util.hamming_distance(binary_feature1, binary_feature2)
