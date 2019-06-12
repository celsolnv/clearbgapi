import os
from io import BytesIO

import numpy as np
from PIL import Image

import tensorflow as tf
import sys
import datetime
 

class RemoveBg(object):
    INPUT_TENSOR_NAME = 'ImageTensor:0'
    OUTPUT_TENSOR_NAME = 'SemanticPredictions:0'
    INPUT_SIZE = 513
    FROZEN_GRAPH_NAME = 'frozen_inference_graph'

    def __init__(self, tarball_path):
        self.graph = tf.Graph()
        module_dir = os.path.dirname(__file__)
        nameFile = os.path.join(module_dir, tarball_path+'/frozen_inference_graph.pb')

        graph_def = None

        graph_def = tf.GraphDef.FromString(open(nameFile, "rb").read()) 

        if graph_def is None:
            raise RuntimeError('Cannot find inference graph in tar archive.')
        with self.graph.as_default():
            tf.import_graph_def(graph_def, name='')
        self.sess = tf.Session(graph=self.graph)

    def run(self, image):
        start = datetime.datetime.now()

        width, height = image.size
        resize_ratio = 1.0 * self.INPUT_SIZE / max(width, height)

        print("Ratio::",end=" ")
        print(resize_ratio)

        target_size = (int(resize_ratio * width), int(resize_ratio * height))
        resized_image = image.convert('RGB').resize(target_size, Image.ANTIALIAS)
        batch_seg_map = self.sess.run(
            self.OUTPUT_TENSOR_NAME,
            feed_dict={self.INPUT_TENSOR_NAME: [np.asarray(resized_image)]})
        seg_map = batch_seg_map[0]

        end = datetime.datetime.now()

        diff = end - start
        print("Time taken to evaluate segmentation is : " + str(diff))

        return resized_image, seg_map

    def removeBackground(self,file):
        try:
            orignal_im = Image.open(BytesIO(file))
        except IOError:
            return
        baseImg, matImg = self.run(orignal_im)

        width, height = baseImg.size
        dummyImg = np.zeros([height, width, 4], dtype=np.uint8)
        for x in range(width):
            for y in range(height):
                color = matImg[y,x]
                (r,g,b) = baseImg.getpixel((x,y))
                if color == 0:
                    dummyImg[y,x,3] = 0
                else :
                    dummyImg[y,x] = [r,g,b,255]
        img = Image.fromarray(dummyImg)
        
        print("======================================================")
        print(type(img))
        print()
        print("======================================================")
        
        return img