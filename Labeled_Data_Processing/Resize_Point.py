#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function
#from lxml import etree
from PIL import Image, ImageOps

import collections
import json
import os

########################################################################################################################
def save_labelmap(filepath, labels):
    with open(filepath, 'w') as fp:
        for idx, label in enumerate(labels):
            fp.write("item {\n")
            fp.write("  id: {}\n".format(idx+1))
            if "'" in label:
                fp.write('  name: "{}"\n'.format(label))
            else:
                fp.write("  name: '{}'\n".format(label))
            fp.write("}\n")

########################################################################################################################
def parse_resize(resize_string):
    pair = []
    temp = resize_string.split('x')
    for x in temp:
        try:
            n = int(x)
            if n > 0:
                pair.append(n)
            else:
                return None
        except ValueError:
            return None
    if len(pair) == 1:
        pair.append(pair[0])
    return tuple(pair[:2])

########################################################################################################################
#def xmlgen(img_basename, size, labels, bndboxes):
#        """
#        generate a pascal voc format xml object
#        parameter(s)
#            filepath    str     image path
#            size        tuple   image size in (w, h)
#            labels      list    class name of bounding boxes
#            bndboxes    list    bounding boxes
#        return
#            xml         lxml.etree.Element
#        """
#
#        def buildxml(r, x):
#            if isinstance(x, dict):
#                for k, v in x.items():
#                    s = etree.SubElement(r, k)
#                    buildxml(s, v)
#            elif isinstance(x, list):
#                for v in x:
#                    s = etree.SubElement(r, 'object')
#                    buildxml(s, v)
#            else:
#                r.text = str(x)
#            return r
#
#        size_dict = collections.OrderedDict()
#        size_dict['width'] = size[0]
#        size_dict['height'] = size[1]
#        size_dict['depth'] = 3
#
#        basic = collections.OrderedDict()
#        basic['folder'] = os.path.basename(os.path.dirname(filepath))
#        basic['filename'] = os.path.basename(filepath)
#        basic['path'] = filepath
#        basic['size'] = size_dict
#        basic['segmented'] = 0
#
#        objects = []
#        for idx, bndbox in enumerate(bndboxes):
#            xmin, ymin, xmax, ymax = bndbox
#            if idx < len(labels):
#                label = labels[idx]
#            else:
#                pass # label should be assigned since labels has one item at least
#            obj = collections.OrderedDict()
#            obj['name'] = label
#            obj['pose'] = 'Unspecified'
#            obj['truncated'] = 0
#            obj['difficult'] = 0
#            obj['bndbox'] = collections.OrderedDict()
#            obj['bndbox']['xmin'] = xmin
#            obj['bndbox']['ymin'] = ymin
#            obj['bndbox']['xmax'] = xmax
#            obj['bndbox']['ymax'] = ymax
#            objects.append(obj)
#
#        xml = etree.Element('annotation')
#        xml = buildxml(xml, basic)
#        xml = buildxml(xml, objects)
#        return xml

########################################################################################################################

def bndbox(points):
        """
        generate bounding box from anchors
        parameter(s)
            points      list    coordinate of all points in (x, y)
        return
            bbox        tuple   (xmin, ymin, xmax, ymax)
        """
        x = [point[0] for point in points]
        y = [point[1] for point in points]
        return min(x), min(y), max(x), max(y)

########################################################################################################################
def resize(target_size, img_filepath, save_dir, quality=95, keep_aspect_ratio=True):
    try:
        img = Image.open(img_filepath)
    except Exception as ex:
        # print(ex)
        return

    img_basename = os.path.basename(img_filepath)
    print(img_basename)

    img_name, img_ext = os.path.splitext(img_basename)
    resized_img_name = '{}_resize_{}x{}'.format(img_name, size[0], size[1])
    resized_img_basename = resized_img_name + img_ext
    resized_img_filepath = os.path.join(save_dir, resized_img_basename)

    original_size = img.size

    # resize and keep aspect ratio
    ratio = min(target_size[0]/original_size[0], target_size[1]/original_size[1])
    new_size = tuple([int(s*ratio) for s in original_size])
    img = img.resize(new_size, Image.BICUBIC)

    # padding to desired size and save imge
    delta_w = target_size[0] - new_size[0]
    delta_h = target_size[1] - new_size[1]
    padding_left   = delta_w // 2
    padding_top    = delta_h // 2
    padding_right  = delta_w - padding_left
    padding_bottom = delta_h - padding_top
    padding = (padding_left, padding_top, padding_right, padding_bottom)
    img = ImageOps.expand(img, padding)
    img.save(resized_img_filepath, quality=quality)

    # modify annotation and save in json format (change shape to bounding box in rectangle)
    jsn_filepath = img_filepath.replace(img_ext, '.json')
    with open(jsn_filepath, 'r') as fp:
        jsn = json.load(fp)

    jsn['imageWidth']  = img.size[0]
    jsn['imageHeight'] = img.size[1]
    jsn['imagePath']   = resized_img_basename

    bndboxes = list()
    labels   = list()
    for shape in jsn['shapes']:
        labels.append(shape['label'])
        points = shape['points']
        for idx, point in enumerate(points):
            x, y = point
            x = int(x * ratio + padding_left)
            y = int(y * ratio + padding_top)
            points[idx] = [x, y]

        ''''''
        # change all shapes to bounding box in rectangle
        # for example, [xmin, ymin], [xmax, ymax]
        xmin, ymin, xmax, ymax = bndbox(shape['points'])
        shape['points'] = [
            [xmin, ymin],
            [xmax, ymax]
        ]
        shape['shape_type'] = 'rectangle'
        

    resized_jsn_basename = resized_img_name + '.json'
    resized_jsn_filepath = os.path.join(save_dir, resized_jsn_basename)
    with open(resized_jsn_filepath, 'w') as fp:
        json.dump(jsn, fp, indent=4)

    ## generate xml in pascal voc annotation and save
    ## collect labels and bounding boxes
    #labels, bndboxes = list(), list()
    #for shape in jsn['shapes']:
    #    labels.append(shape['label'])
    #    bndboxes.append(bndbox(shape['points']))
    ## generate xml file
    #resized_xml_basename = resized_img_name + '.xml'
    #resized_xml_filepath = os.path.join(save_dir, resized_xml_basename)
    #with open(resized_xml_filepath, 'w') as fp:
    #    fp.write(etree.tostring(xmlgen(resized_img_basename, img.size, labels, bndboxes), encoding='utf-8', pretty_print=True).decode('utf-8'))

    return labels

####################################################################################################
if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Resize images in a folder')
    parser.add_argument('--input',    '-i', help='input image folder', required=True)
    parser.add_argument('--output',   '-o', help='output image folder')
    parser.add_argument('--size',     '-s', help='size in widthxheight format, i.e., 600x600', default='600x600')
    parser.add_argument('--labelmap', '-l', help='generate labelmap', action='store_true')
    parser.add_argument('--quality',  '-q', help='save quality',   type=int, default=95)
    args = parser.parse_args()
    #print(args)

    # Validate parameters
    input_path = os.path.abspath(args.input)
    if not os.path.isdir(args.input):
        print('--input ({}) must be a folder.'.format(args.input))
        sys.exit(1)

    size = parse_resize(args.size)
    if size[0] < 2 or size[1] < 2:
        print('--size ({}) must grater than 2x2.'.format(args.size))
        sys.exit(1)

    if args.output is None:
        args.output = '{}_resize_{}x{}'.format(input_path, size[0], size[1])
        os.makedirs(args.output, mode=0o777, exist_ok=True)
    if not os.path.isdir(args.output):
        print('--output ({}) must be a folder.'.format(args.output))
        sys.exit(1)
    output_path = os.path.abspath(args.output)

    label_list = list()
    for root, _, basenames in os.walk(input_path):
        for basename in basenames:
            filepath = os.path.join(root, basename)
            labels = resize(size, filepath, output_path, quality=args.quality)
            if labels is None: continue
            for label in labels:
                if label in label_list: continue
                label_list.append(label)

    if args.labelmap:
        filepath = os.path.dirname(input_path) # parent dir of input
        filepath = os.path.join(filepath, 'label_map.pbtxt')
        save_labelmap(filepath, label_list)