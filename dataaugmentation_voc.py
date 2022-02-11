import xml.etree.ElementTree as ET
import os
import imgaug as ia
import numpy as np
import shutil
from tqdm import tqdm
from PIL import Image
from imgaug import augmenters as iaa
ia.seed(1)
def read_xml_annotation(root, image_id):
    in_file = open(os.path.join(root, image_id))
    tree = ET.parse(in_file)
    root = tree.getroot()
    bndboxlist = []

    for object in root.findall('object'):  # 找到root節點下的所有country節點
        bndbox = object.find('bndbox')  # 子節點下節點rank的值

        xmin = int(bndbox.find('xmin').text)
        xmax = int(bndbox.find('xmax').text)
        ymin = int(bndbox.find('ymin').text)
        ymax = int(bndbox.find('ymax').text)
        # print(xmin,ymin,xmax,ymax)
        bndboxlist.append([xmin, ymin, xmax, ymax])
        # print(bndboxlist)

    bndbox = root.find('object').find('bndbox')
    return bndboxlist

#-------------------------------------------------#
# [Read the bounding boxes coordinate of the original image]
# Read xml file and using ElementTree to decode xml file, then found each coordinate
#-------------------------------------------------#
# (506.0000, 330.0000, 528.0000, 348.0000) -> (520.4747, 381.5080, 540.5596, 398.6603)
def change_xml_annotation(root, image_id, new_target):
    new_xmin = new_target[0]
    new_ymin = new_target[1]
    new_xmax = new_target[2]
    new_ymax = new_target[3]

    in_file = open(os.path.join(root, str(image_id) + '.xml'))  # 這裡的root分別由兩個意思
    tree = ET.parse(in_file)
    xmlroot = tree.getroot()
    object = xmlroot.find('object')
    bndbox = object.find('bndbox')
    xmin = bndbox.find('xmin')
    xmin.text = str(new_xmin)
    ymin = bndbox.find('ymin')
    ymin.text = str(new_ymin)
    xmax = bndbox.find('xmax')
    xmax.text = str(new_xmax)
    ymax = bndbox.find('ymax')
    ymax.text = str(new_ymax)
    tree.write(os.path.join(root, str("%06d" % (str(id) + '.xml'))))


def change_xml_list_annotation(root, image_id, new_target, saveroot, id):
    in_file = open(os.path.join(root, str(image_id) + '.xml'))  # 這裡的root分別由兩個意思
    tree = ET.parse(in_file)
    #修改DA後的xml文件中的filename
    elem = tree.find('filename')
    elem.text = (str(id) + '.jpg')
    xmlroot = tree.getroot()
    #修改DA後的xml文件中的path
    elem = tree.find('path')
    if elem != None:
        elem.text = ('F:/DataSet/SnacksMIT/AUG/JPEGImages/' + str(id) + '.jpg')

    index = 0
    for object in xmlroot.findall('object'):  # 找到root節點下的所有country節點
        bndbox = object.find('bndbox')  # 子節點下節點rank的值

        # xmin = int(bndbox.find('xmin').text)
        # xmax = int(bndbox.find('xmax').text)
        # ymin = int(bndbox.find('ymin').text)
        # ymax = int(bndbox.find('ymax').text)

        new_xmin = new_target[index][0]
        new_ymin = new_target[index][1]
        new_xmax = new_target[index][2]
        new_ymax = new_target[index][3]

        xmin = bndbox.find('xmin')
        xmin.text = str(new_xmin)
        ymin = bndbox.find('ymin')
        ymin.text = str(new_ymin)
        xmax = bndbox.find('xmax')
        xmax.text = str(new_xmax)
        ymax = bndbox.find('ymax')
        ymax.text = str(new_ymax)

        index = index + 1

    tree.write(os.path.join(saveroot, str(id + '.xml')))


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
    IMG_DIR = "./image-600x600-voc/JPEGImages/"
    XML_DIR = "./image-600x600-voc/Annotations/"

    AUG_XML_DIR = "./AUG/Annotations/"  # 儲存DA後的xml文件資料夾路徑
    try:
        shutil.rmtree(AUG_XML_DIR)
    except FileNotFoundError as e:
        a = 1
    mkdir(AUG_XML_DIR)

    AUG_IMG_DIR = "./AUG/JPEGImages/"  # 儲存DA後的影像文件資料夾路徑
    try:
        shutil.rmtree(AUG_IMG_DIR)
    except FileNotFoundError as e:
        a = 1
    mkdir(AUG_IMG_DIR)

    AUGLOOP = 10  # 每張影像進行增強的數量

    boxes_img_aug_list = []
    new_bndbox = []
    new_bndbox_list = []

    #-------------------------------------------------#
    # [ A sequential of processing image]
    # 影像增强
    # Ref:https://imgaug.readthedocs.io/en/latest/index.html
    #-------------------------------------------------#
    sometimes = lambda aug: iaa.Sometimes(0.5, aug)
    seq = iaa.Sequential([
        #iaa.Invert(0.5),
        #sometimes(iaa.Cutout(nb_iterations=2)),
        #sometimes(iaa.Jigsaw(nb_rows=(10),nb_cols=(10))),
        #sometimes(iaa.Jigsaw(nb_rows=(1,4),nb_cols=(1,4))),
        sometimes(iaa.Sharpen(alpha=(0.0, 1.0), lightness=(0.75, 2.0))),
        sometimes(iaa.CoarseDropout((0.0, 0.05), size_percent=(0.02, 0.25))),
        sometimes(iaa.Add((-40, 40))),
        sometimes(iaa.LinearContrast((0.4, 1.6))),
        sometimes(iaa.Cutout(nb_iterations=2)),
        #sometimes(iaa.Fliplr(0.5)),
        #sometimes(iaa.Flipud(0.5)),
        sometimes(iaa.Multiply((1.2, 1.5))),  # change brightness, doesn't affect BBs
        sometimes(iaa.GaussianBlur(sigma=(0, 3.0))),  # iaa.GaussianBlur(0.5),
        #sometimes(iaa.Rotate((-45,180))),
        #sometimes(iaa.Affine(translate_px={"x": 15, "y": 15}, scale=(0.8, 0.95),))  # translate by 40/60px on x/y axis, and scale to 50-70%, affects BBs
    ])

    for name in tqdm(os.listdir(XML_DIR), desc='Processing'):
        bndbox = read_xml_annotation(XML_DIR, name)
        # 保存原xml文件
        shutil.copy(os.path.join(XML_DIR, name), AUG_XML_DIR)
        # 保存原始影像
        og_img = Image.open(IMG_DIR+'/'+name[:-4] + '.jpg')
        og_img.convert('RGB').save(AUG_IMG_DIR + name[:-4] + '.jpg', 'JPEG')
        og_xml = open(os.path.join(XML_DIR, name)) 
        tree = ET.parse(og_xml)
        #修改DA後的xml文件中的filename
        elem = tree.find('filename')
        elem.text = (name[:-4] + '.jpg')
        tree.write(os.path.join(AUG_XML_DIR, name))

        #-------------------------------------------------#
        # [ Counting the coordinate after modify bounding box]
        #-------------------------------------------------#
        for epoch in range(AUGLOOP):
            seq_det = seq.to_deterministic()  # 保持影像與標記座標同步進行更改
            # 讀取影像
            img = Image.open(os.path.join(IMG_DIR, name[:-4] + '.jpg'))
            # sp = img.size
            img = np.asarray(img)
            # bndbox 座標處理
            for i in range(len(bndbox)):
                #-------------------------------------------------#
                # [BoundingBoxes sequience]
                # (https://imgaug.readthedocs.io/en/latest/source/examples_bounding_boxes.html#)
                #-------------------------------------------------#
                bbs = ia.BoundingBoxesOnImage([
                    ia.BoundingBox(x1=bndbox[i][0], y1=bndbox[i][1], x2=bndbox[i][2], y2=bndbox[i][3]),
                ], shape=img.shape)

                bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]
                boxes_img_aug_list.append(bbs_aug)

                # new_bndbox_list:[[x1,y1,x2,y2],...[],[]]
                n_x1 = int(max(1, min(img.shape[1], bbs_aug.bounding_boxes[0].x1)))
                n_y1 = int(max(1, min(img.shape[0], bbs_aug.bounding_boxes[0].y1)))
                n_x2 = int(max(1, min(img.shape[1], bbs_aug.bounding_boxes[0].x2)))
                n_y2 = int(max(1, min(img.shape[0], bbs_aug.bounding_boxes[0].y2)))
                if n_x1 == 1 and n_x1 == n_x2:
                    n_x2 += 1
                if n_y1 == 1 and n_y2 == n_y1:
                    n_y2 += 1
                if n_x1 >= n_x2 or n_y1 >= n_y2:
                    print('error', name)
                new_bndbox_list.append([n_x1, n_y1, n_x2, n_y2])
            # 儲存DA後的影像
            image_aug = seq_det.augment_images([img])[0]
            path = os.path.join(AUG_IMG_DIR,
                                str(str(name[:-4]) + '_' + str(epoch)) + '.jpg')
            image_auged = bbs.draw_on_image(image_aug, size=0)
            Image.fromarray(image_auged).convert('RGB').save(path) 

            # 儲存DA後的XML→FileName
            change_xml_list_annotation(XML_DIR, name[:-4], new_bndbox_list, AUG_XML_DIR,
                                        str(name[:-4]) + '_' + str(epoch))
            # print(str(str(name[:-4]) + '_' + str(epoch)) + '.jpg')
            new_bndbox_list = []
    print('Finish!')

'''
[Reference Info.]
: Artical: [voc数据集对有标签的数据集数据增强](https://blog.csdn.net/m0_37940759/article/details/115212083)
: Author: CodingWZP
: Email: codingwzp@gmail.com
: Date: 2021-08-06 10:51:35
: LastEditTime: 2021-08-09 10:53:43
: Description: Image augmentation with label.
'''