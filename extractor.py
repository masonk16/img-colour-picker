#!/usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import cv2
import extcolors
from colormap import rgb2hex


class Extractor:
    """
    Extracts colours from image.
    """

    def resize(self, input_image, resize, tolerance, zoom):
        """
        Resizes image.
        :return: resized image.
        """
        # background
        bg = 'bg.png'
        fig, ax = plt.subplots(figsize=(192, 108), dpi=10)
        fig.set_facecolor('white')
        plt.savefig(bg)
        plt.close(fig)

        # resize
        output_width = resize
        img = Image.open(input_image)
        if img.size[0] >= resize:
            wpercent = (output_width / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((output_width, hsize), Image.ANTIALIAS)
            resize_name = 'resize_' + input_image
            img.save(resize_name)
        else:
            resize_name = input_imag
