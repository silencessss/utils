# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 11:06:11 2020

@author: Peter Chan
"""
import cv2
import os

def Video2Image(path_video,path_output_image):
    interval = 1 # 保存時的fps間隔
    frame_count = 1 # 保存fps的索引
    frame_index = 1 # 原影片的索引，與interval*frame_count = frame_index 
    cap = cv2.VideoCapture(path_video)
    
    if cap.isOpened():
        success = True
    else:
        success = False
        print("[Info] Video read fail!")

    while(True):
        success, frame = cap.read()
        cv2.waitKey(1)
        #if success is False:
        #    print("---> [Info] Fail in %d fps:" % frame_index)
        #    break     
        print("---> [Info] Read %d fps:" % frame_index, success)
        if(frame_index%interval)==0:
            print('frame_count',frame_count)
            path_output_image_name = os.path.join(path_output_image,str(frame_count))
            path_output_image_name = path_output_image_name+'.jpg'
            print('###',path_output_image_name)
            try:
                frame = cv2.rotate(frame,cv2.ROTATE_180)
                cv2.imwrite(path_output_image_name,frame,[cv2.IMWRITE_JPEG_QUALITY, 100])
                print('#----------Write Success!----------#')
            except:
                print('#----------Write    Fail!----------#')
            frame_count+=1
        frame_index+=1
'''
video = cv2.VideoCapture('F:/DataSet/Blind_Spot_20220329/Blind_Spot_20220329/Right/GH010670/GH010670.MP4') # 23.97602537435857
fps = video.get(cv2.CAP_PROP_FPS)
print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
video.release()
'''
if __name__=='__main__':
    path_input_dir = r'F:/DataSet/Blind_Spot_20220329/Blind_Spot_20220329/Right/GH010670'
    path_output_dir = r'F:/DataSet/Blind_Spot_20220329/Blind_Spot_20220329/Right_images/GH010670'
    count=1
    for root, _, basenames in os.walk(path_input_dir):
        for basename in basenames:
            print(basename.split('.')[1])
            if(basename.split('.')[1]=='MP4'):#要處理的附檔名
                print('processing...',count)
                path_video = os.path.join(path_input_dir, basename)
                path_output_image = os.path.join(path_output_dir, basename.split('.')[0]+'\\')
                print('####',path_output_image)
                if not os.path.isdir(os.path.dirname(path_output_image)):
                    print('Build: ',os.path.dirname(path_output_image))
                    os.makedirs(os.path.dirname(path_output_image))
                    print('#----------Build Success!----------#')
                Video2Image(path_video,path_output_image)
                count+=1
    print('#----------Processing Done!----------#')
