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

    def resize(self, filename):
        """
        Resizes image.
        :param filename: file to be resized.
        :return: resized image.
        """
        input_name = filename
        output_width = 900  # set the output size
        img = Image.open(input_name)
        wpercent = (output_width / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((output_width, hsize), Image.ANTIALIAS)

        # save
        resize_name = 'resize_' + input_name  # the resized image name
        img.save(resize_name)  # output location can be specified before resize_name

        # read
        plt.figure(figsize=(9, 9))
        self.img_url = resize_name
        img = plt.imread(self.img_url)
        plt.imshow(img)
        plt.axis('off')
        plt.show()

        return self.img_url

    def colour_ex(self):
        self.colors_x = extcolors.extract_from_path(self.img_url, tolerance=11, limit=11)
        return self.colors_x

    def color_to_df(self):
        colors_pre_list = str(self.colors_x).replace('([(', '').split(', (')[0:-1]
        df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
        df_percent = [i.split('), ')[1].replace(')', '') for i in colors_pre_list]

        # convert RGB to HEX code
        df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(", "")),
                               int(i.split(", ")[1]),
                               int(i.split(", ")[2].replace(")", ""))) for i in df_rgb]

        self.df_colour = pd.DataFrame(zip(df_color_up, df_percent), columns=['c_code', 'occurence'])
        return self.df_colour

    def colours_chart(self):
        list_color = list(self.df_colour['c_code'])
        list_precent = [int(i) for i in list(self.df_colour['occurence'])]
        text_c = [c + ' ' + str(round(p * 100 / sum(list_precent), 1)) + '%' for c, p in zip(list_color,
                                                                                             list_precent)]
        fig, ax = plt.subplots(figsize=(90, 90), dpi=10)
        wedges, text = ax.pie(list_precent,
                              labels=text_c,
                              labeldistance=1.05,
                              colors=list_color,
                              textprops={'fontsize': 120, 'color': 'black'}
                              )
        plt.setp(wedges, width=0.3)

        # create space in the center
        plt.setp(wedges, width=0.36)

        ax.set_aspect("equal")
        fig.set_facecolor('white')
        return self.plt.show()
