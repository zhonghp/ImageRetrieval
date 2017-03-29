#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: vasezhong
# @Date:   2017-03-28 19:51:08
# @Last Modified by:   vasezhong
# @Last Modified time: 2017-03-29 11:22:55

import cv2
import numpy as np


def bgr2rgb(img_bgr):
    if img_bgr is not None:
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    else:
        img_rgb = None
    return img_rgb


def rgb2bgr(img_rgb):
    if img_rgb is not None:
        img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    else:
        img_bgr = None
    return img_bgr


def gif2jpg(img_path):
    img = Image.open(img_path)
    if img is not None:
        frames = [f for f in ImageSequence.Iterator(img)]
        # choose the first frame
        pil_image = frames[0].convert('RGB')
        cv_image = np.array(pil_image)
        img_bgr = cv_image[:, :, ::-1]
    else:
        img_bgr = None
    return img_bgr


def cosine_similarity(feat1, feat2):
    return np.dot(feat1, feat2) / np.linalg.norm(feat1) / np.linalg.norm(feat2)


def hamming_distance(feat1, feat2):
    return np.count_nonzero(feat1 != feat2)
