import xml.etree.ElementTree as ET
import os
import imgaug as ia
from imgaug.augmenters.flip import Flipud
import numpy as np
import shutil
from tqdm import tqdm
from PIL import Image
from imgaug import augmenters as iaa
ia.seed(1)
def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符號
    path = path.rstrip("\\")
    # 判斷路徑是否存在, 存在True, 不存在False
    isExists = os.path.exists(path)
    # 判斷结果
    if not isExists:
        # 若目錄不存在，則建立目錄
        # 建立目錄的操作函数
        os.makedirs(path)
        print(path + ' create success!')
        return True
    else:
        # 若目錄存在，則不建立且提示已存在
        print(path + ' it exist!')
        return False


if __name__ == "__main__":
    #-------------------------------------------------#
    # [ File path setting ]
    #-------------------------------------------------#
    IMG_DIR = r'F:/DataSet/DataSet_Acne/AcneECK/New_Order/AcneECK003/Original/4'
    
    AUG_IMG_DIR = r'F:/DataSet/DataSet_Acne/AcneECK/New_Order/AcneECK003/AUG/4'  # 儲存DA後的影像文件資料夾路徑
    try:
        shutil.rmtree(AUG_IMG_DIR)
    except FileNotFoundError as e:
        a = 1
    mkdir(AUG_IMG_DIR)

    AUGLOOP =6  # 每张影像增强的数量

    boxes_img_aug_list = []


    #-------------------------------------------------#
    # [ A sequential of processing image]
    # 影像增强
    # Ref:https://imgaug.readthedocs.io/en/latest/index.html
    #-------------------------------------------------#
    sometimes = lambda aug: iaa.Sometimes(0.5, aug)
    seq = iaa.Sequential([
        #iaa.Invert(0.5),
        #sometimes(iaa.Cutout(nb_iterations=2)),
        sometimes(iaa.Jigsaw(nb_rows=(10),nb_cols=(10))),
        sometimes(iaa.Jigsaw(nb_rows=(1,4),nb_cols=(1,4))),
        #sometimes(iaa.CoarseDropout((0.0, 0.05), size_percent=(0.02, 0.25))),
        sometimes(iaa.Fliplr(0.5)),
        sometimes(iaa.Flipud(0.5)),
        #iaa.Multiply((1.2, 1.5)),  # change brightness, doesn't affect BBs
        #iaa.GaussianBlur(sigma=(0, 3.0)),  # iaa.GaussianBlur(0.5),
        sometimes(iaa.Rotate((-45,180))),
        sometimes(iaa.Affine(
            translate_px={"x": 15, "y": 15},
            scale=(0.8, 0.95),
        ))  # translate by 40/60px on x/y axis, and scale to 50-70%, affects BBs
    ])

    for name in tqdm(os.listdir(IMG_DIR), desc='Processing'):
        print(name)
        print('###',name[:-4])
        print(IMG_DIR+'/'+name[:-5] + '.jpeg')

        # 保存原始影像
        try:
            og_img = Image.open(IMG_DIR+'/'+name[:-4] + '.jpg')
        except:
            try:
                og_img = Image.open(IMG_DIR+'/'+name[:-4] + '.png')
            except:
                og_img = Image.open(IMG_DIR+'/'+name[:-5] + '.jpeg')
        og_img.convert('RGB').save(AUG_IMG_DIR + name[:-4] + '.jpg', 'JPEG')


        #-------------------------------------------------#
        # [ Counting the coordinate after modify bounding box]
        #-------------------------------------------------#
        for epoch in range(AUGLOOP):
            # 讀取影像
            try:
                img = Image.open(os.path.join(IMG_DIR, name[:-5] + '.jpeg'))
            except:
                try:
                    img = Image.open(IMG_DIR+'/'+name[:-4] + '.png')
                except:
                    img = Image.open(IMG_DIR+'/'+name[:-4] + '.jpg')
            # sp = img.size
            img = img.resize((1600,1600))
            img = np.asarray(img)
            #print(img)
            # 儲存DA後的影像
            image_aug = seq.augment_images([img])[0]
            path = os.path.join(AUG_IMG_DIR,
                                str(str(name[:-4]) + '_' + str(epoch)) + '.jpg')
            Image.fromarray(image_aug).convert('RGB').save(path) 

            # print(str(str(name[:-4]) + '_' + str(epoch)) + '.jpg')
            new_bndbox_list = []
    print('Finish!')


'''
[Reference Info.]
Artical: [voc数据集对有标签的数据集数据增强](https://blog.csdn.net/m0_37940759/article/details/115212083)
Author: CodingWZP
Email: codingwzp@gmail.com
Date: 2021-08-06 10:51:35
LastEditTime: 2021-08-09 10:53:43
Description: Image augmentation with label.
'''