#!/usr/bin/env python
# Name: utils.py
# Time:9/27/16 2:57 PM
# Author:luo1fly

from xml.etree.ElementTree import ElementTree, ElementTree, Element, SubElement, tostring
from PIL import Image
import subprocess
import os
import time

# import custom modules above

ROOT_PATH = '/www/htdocs'


def generate_xml_by_sku(sku_lst):
    sku_info = ElementTree()
    sku_img = Element('sku_img', {'version': '1.0'})
    sku_info._setroot(sku_img)

    SubElement(sku_img, 'host').text = 'img.xxx.com'
    SubElement(sku_img, 'host').text = 'img.xxx.com'
    SubElement(sku_img, 'host').text = 'img.xxx.com'

    SubElement(sku_img, 'linkprefix').text = 'productimages'
    SubElement(sku_img, 'linkprefix').text = 'productImages'
    SubElement(sku_img, 'linkprefix').text = 'ProductImages'

    for s in sku_lst:
        sku = Element('sku')
        sku_img.append(sku)

        SubElement(sku, 'no').text = s

        cmd = 'ls -v  %s/images/%s/%s/%s/sku_%s_*' % (ROOT_PATH, s[0], s[1], s[2], s)
        try:
            b = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as e:
            continue
        path_lst = b.decode('utf8').split('\n')
        print(path_lst)
        for path in path_lst:
            if path:
                try:
                    im = Image.open(path)
                except FileNotFoundError as e:
                    continue
                img = Element('img')
                sku.append(img)

                SubElement(img, 'name').text = os.path.basename(path)
                # sku_123796_1.jpg
                width, height = im.size
                SubElement(img, 'width').text = str(width)
                # 600
                SubElement(img, 'height').text = str(height)
                # 600
                tm = os.stat(path).st_mtime
                mtm = time.gmtime(tm)
                str_utc = time.strftime('%Y-%m-%d %H:%M:%S', mtm)
                SubElement(img, 'last-modified').text = str_utc
                # 2016-09-22 08:50:27
                size = os.stat(path).st_size
                SubElement(img, 'size').text = str(size)
                # 27625

    return tostring(sku_img)
