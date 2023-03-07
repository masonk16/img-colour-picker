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
        self.list_colour = list(self.df_colour['c_code'])
        list_precent = [int(i) for i in list(self.df_colour['occurence'])]
        text_c = [c + ' ' + str(round(p * 100 / sum(list_precent), 1)) + '%' for c, p in zip(self.list_colour,
                                                                                             list_precent)]
        fig, ax = plt.subplots(figsize=(90, 90), dpi=10)
        wedges, text = ax.pie(list_precent,
                              labels=text_c,
                              labeldistance=1.05,
                              colors=self.list_colour,
                              textprops={'fontsize': 120, 'color': 'black'}
                              )
        plt.setp(wedges, width=0.3)

        # create space in the center
        plt.setp(wedges, width=0.36)

        ax.set_aspect("equal")
        fig.set_facecolor('white')
        return self.plt.show()

    def colour_palette(self):
        # create background color
        fig, ax = plt.subplots(figsize=(192, 108), dpi=10)
        fig.set_facecolor('white')
        plt.savefig('bg.png')
        plt.close(fig)

        # create color palette
        bg = plt.imread('bg.png')
        fig = plt.figure(figsize=(90, 90), dpi=10)
        ax = fig.add_subplot(1, 1, 1)

        x_posi, y_posi, y_posi2 = 320, 25, 25
        for c in self.list_colour:
            if self.list_colour.index(c) <= 5:
                y_posi += 125
                rect = patches.Rectangle((x_posi, y_posi), 290, 115, facecolor=c)
                ax.add_patch(rect)
                ax.text(x=x_posi + 360, y=y_posi + 80, s=c, fontdict={'fontsize': 150})
            else:
                y_posi2 += 125
                rect = patches.Rectangle((x_posi + 800, y_posi2), 290, 115, facecolor=c)
                ax.add_artist(rect)
                ax.text(x=x_posi + 1160, y=y_posi2 + 80, s=c, fontdict={'fontsize': 150})

        ax.axis('off')
        plt.imshow(bg)
        plt.tight_layout()
