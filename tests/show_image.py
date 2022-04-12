# -*- coding: utf-8 -*-


from matplotlib import pyplot as plt
import numpy as np
import matplotlib.image as im
import os

def read_path(file_pathname):
    #遍历该目录下的所有图片文件
    # # 读取jpg格式图片
    # for filename in os.listdir(file_pathname):
    #     # img = im.imread(os.path.join(file_pathname, filename))
    #     # print(r"{}".format(f_filename))
    #     print(filename)
    #     img = file_pathname + "\\" + filename
    #     print(img)
    #     img2 = im.imread(img)
    #
    #     plt.cla()
    #     plt.imshow(img2)
    #     plt.axis('off')


        # 读取png格式图片
    for filename in os.listdir(file_pathname):
        print(filename)
        img = file_pathname + "\\" + filename
        print(img)
        img2 = im.imread(img)

        plt.cla()
        plt.imshow(img2)
        plt.axis('off')


        if filename == initial_name:
            plt.pause(2)
        else:
            plt.pause(0.1)

#初始化图片名称
# #jpg格式
# initial_name = "0WSN_initial.jpg"
#svg格式
initial_name = "0WSN_initial.png"

#读取的目录

# read_path("./image_jpg")
read_path("./image_png")

