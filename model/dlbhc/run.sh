#!/usr/bin/env sh
# @Author: vasezhong
# @Date:   2017-03-27 19:37:43
# @Last Modified by:   vasezhong
# @Last Modified time: 2017-03-28 16:47:52

caffe train --solver=solver.prototxt --weights=../bvlc_alexnet/bvlc_alexnet.caffemodel --gpu=1