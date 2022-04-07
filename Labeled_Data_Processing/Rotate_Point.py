#!/usr/bin/env python
# -*- utf-8 -*-
from __future__ import division, print_function
from PIL import Image

import copy
import json
import numpy as np
import os

########################################################################################################################
class ImageRotater(object):
    def __init__(self, input_path, output_path, angles=[a for a in range(360)], save_quality=95):
        self.input_path = input_path
        self.output_path = output_path
        self.angles = angles
        self.quality = save_quality

    def initiate(self, img_basename):
        self.img_basename = img_basename
        img_filepath = os.path.join(self.input_path, img_basename)
        try:
            self.img = Image.open(img_filepath)
        except:
            return False

        #print(self.img.format)
        #----------------#
        # Here to modify image format
        #----------------#
        if self.img.format not in ('MPO', 'JPEG'):
            return False

        self.img_name, img_ext = os.path.splitext(img_basename)
        jsn_filepath = img_filepath.replace(img_ext, '.json')

        try:
            with open(jsn_filepath, 'r') as fp:
                try:
                    self.jsn = json.load(fp)
                except:
                    return False
        except:
            return False

        return True

    def rotxy(self, xy, center_ori, center_rot, angle):
        """
        rotate a point and return the coordinate
        parameter(s)
            xy          np.array    coordinate of the point
            center_ori  np.array    coordinate of center point of original image
            center_rot  np.array    coordinate of center point of rotated image
            angle       int         rotate angle
        return
            rot_xy      np.array    coordinate of the rotated point
        """
        org = xy - center_ori
        r   = np.deg2rad(angle)
        rot = np.array([ org[0]*np.cos(r) + org[1]*np.sin(r),
                        -org[0]*np.sin(r) + org[1]*np.cos(r)])
        rot_xy = rot + center_rot

        return int(rot_xy[0]), int(rot_xy[1])

    def run(self):
        print(self.img_basename)

        center_ori = np.array(self.img.size) / 2
        for angle in self.angles:
            #print('angle...',self.angles)
            rotimg_basename = '{}_{:03d}.jpg'.format(self.img_name, angle)
            rotjsn_basename = '{}_{:03d}.json'.format(self.img_name, angle)
            rotimg_filepath = os.path.join(self.output_path, rotimg_basename)
            rotjsn_filepath = os.path.join(self.output_path, rotjsn_basename)

            rotimg = self.img.rotate(angle, resample=Image.BICUBIC, expand=True)
            rotimg.save(rotimg_filepath, quality=self.quality)
            center_rot = np.array(rotimg.size) / 2

            rotjsn = copy.deepcopy(self.jsn)
            rotjsn['imagePath'] = rotimg_basename
            rotjsn['imageWidth']  = rotimg.size[0]
            rotjsn['imageHeight'] = rotimg.size[1]
            for shape in rotjsn['shapes']:
                rotpoints = []
                points = shape['points']
                for point in points:
                    x, y = self.rotxy(np.array(point), center_ori, center_rot, angle)
                    rotpoints.append([x, y])
                shape['points'] = rotpoints
            with open(rotjsn_filepath, 'w') as fp:
                json.dump(rotjsn, fp, indent=4)

            #rectangle or polygon
            if angle == 0 and self.jsn['shapes'][0]['shape_type'] != 'polygon':
                break

####################################################################################################
if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Rotate images in a folder')
    parser.add_argument('--input',   '-i', help='input image folder', required=True)
    parser.add_argument('--output',  '-o', help='output image folder')
    parser.add_argument('--angle',   '-a', help='angle per step', type=int, default=5)
    parser.add_argument('--stop',    '-p', help='stop angle',     type=int, default=359)
    parser.add_argument('--quality', '-q', help='save quality',   type=int, default=95)
    args = parser.parse_args()
    print(args)

    # Validate parameters
    input_path = os.path.abspath(args.input)
    #print(input_path)
    if not os.path.isdir(args.input):
        print('--input ({}) must be a folder.'.format(args.input))
        sys.exit(1)

    if args.output is None:
        args.output = input_path + '_rotate'
        os.makedirs(args.output, mode=0o777, exist_ok=True)
    if not os.path.isdir(args.output):
        print('--output ({}) must be a folder.'.format(args.output))
        sys.exit(1)
    output_path = os.path.abspath(args.output)

    if args.angle < 1 or args.angle > 359:
        print('--angle ({}) must in range 1-359.'.format(args.angle))
        sys.exit(1)

    if args.stop <= args.angle or args.angle > 359:
        print('--stop ({}) must in range {}-359.'.format(args.stop, args.angle))

    angles = [angle for angle in range(0, args.stop, args.angle)]

    import time
    from multiprocessing import cpu_count, Process

    print('Collecting image file in {}'.format(input_path))
    rotaters = []
    for root, _, basenames in os.walk(input_path):
        for basename in basenames:
            filepath = os.path.join(root, basename)
            #print('angles == ',angles)
            rotater = ImageRotater(input_path, output_path, angles=angles, save_quality=args.quality)
            if not rotater.initiate(basename): continue
            rotaters.append(rotater)
    total = len(rotaters)
    print('Total {}-image found'.format(total))

    cpu = cpu_count()
    total_process_time = 0.
    processes = list()
    for idx, rotater in enumerate(rotaters):
        t0 = time.time()
        counter = idx + 1
        p = Process(target=rotater.run)
        p.start()
        processes.append(p)

        if (counter % cpu == 0) or (counter == total):
            for p in processes: p.join() # wait for all processes are done
            processes = list()
            process_time = time.time() - t0
            total_process_time =  total_process_time + process_time
            print('Process time: {:.3f} (total: {:.3f})'.format(process_time, total_process_time))