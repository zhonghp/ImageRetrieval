#!/usr/bin/env sh
# @Author: vasezhong
# @Date:   2017-03-28 14:45:30
# @Last Modified by:   vasezhong
# @Last Modified time: 2017-03-28 14:46:20

caffe train --solver=solver.prototxt --weights=VGG_ILSVRC_19_layers.caffemodel --gpu=2
