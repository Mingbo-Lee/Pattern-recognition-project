#避免栈溢
import tensorflow as tf
tf.compat.v1.disable_eager_execution()
gpus=tf.config.experimental.list_physical_devices(device_type='GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu,True)
#设定结束

import os
import numpy as np
import pandas as pd
from keras import models
from collections import defaultdict
import json
import datetime
from face_detect import face_tect

#加载模型
model=models.load_model("../deeplearning_model/facenet_inception_resnetv1.h5")

#------------UI -init----
from PyQt5.QtWidgets import QMainWindow, QApplication
from faceRecUi import Ui_MainWindow
from PyQt5 import QtCore, QtGui
import sys
import cv2
import time
import tkinter


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)


app = QApplication(sys.argv)
main = Main()
main.show()



def camCtrl(cap, main):
    while (main.btn1_click % 2 != 0):
        cv2.waitKey(1)
        ret, img = cap.read()
        main.updateStreamSrc(img)


def callbackClose():
    tkinter.messagebox.showwarning(title='警告', message='点击了关闭按钮')
    sys.exit(0)

#UI-end
#--人脸检测----#


# 需要引擎开启的功能


def  get_features_from_database(filedir):
    features=defaultdict(list)
    for name_filedirs in os.listdir(filedir):
        for imgName in os.listdir(os.path.join(filedir,name_filedirs)):
            img = cv2.imread(os.path.join(filedir,name_filedirs,imgName))
            face_img=np.expand_dims(img,axis=0)
            embedding=model.predict(face_img)
            features[name_filedirs].append(embedding)
            msg="log: Init: Name: "+os.path.join(name_filedirs, imgName)+"  features extracted Successfully!"
            print(msg)
            main.textBrowser.append(msg)
    msg = "人脸识别系统初始化完毕，可以开始签到！"
    print(msg)
    main.textBrowser.append(msg)
    return features

def face_embeddings_compares(embedding1,embedding2):
    distance = np.sqrt(np.sum(np.square(embedding1 - embedding2), axis=-1))
    return distance[0]


def face_recognition(img,database_features):
    statu, faces ,face_box = face_tect(img)
    face_embeddings=list()
    ids_list=list()
    if statu == True:
        flag=True
        for i in range(faces.shape[0]):
            face_img=np.expand_dims(faces[i],axis=0)
            embedding = model.predict(face_img)
            face_embeddings.append(embedding)
    else:
        return False,None,None,None
    face_threshold = 1.00
    #希望获取的两个指标
    face_name_list=["unknown"]*faces.shape[0]
    distance_min_list=[10]*faces.shape[0]

    for face_index in range(len(face_embeddings)):
        embedding=face_embeddings[face_index]
        for id in database_features.keys():
            for i in range(len(database_features[id])):
                distance= face_embeddings_compares(embedding,database_features[id][i])
                if distance<distance_min_list[face_index]:
                    distance_min_list[face_index]=distance
                    if distance_min_list[face_index] < face_threshold:
                        face_name_list[face_index] = id
    return True, face_name_list,distance_min_list,face_box

#--------签到系统预处理----------

def load_name_sheet(sheet_dir):
    json_name=open(sheet_dir, 'r')
    name_dict = json.load(json_name)
    for key in name_dict.keys():
        name_dict[key]['check_in_status']=False
        name_dict[key]['Check_in_time']=''
    return name_dict


def Video_Stram():



    # video = "http://admin:admin@192.168.31.136:8080"  # 此处@后的ipv4 地址需要改为app提供的地址
    #video = "rtsp://192.168.31.136:8080/video/h264"
    #video = "http://192.168.31.136:8080/video/mjpeg"
    #video = "rtsp://192.168.1.143:8080/video/h264"
    video=0
    cap = cv2.VideoCapture(video)

    # 抓取摄像头视频图像
    #特征初始化
    face_features = get_features_from_database("../Datasets/DataSet-PRface2021_160_lfw")
    #姓名表初始化
    name_sheet = load_name_sheet("name_sheet.json")


    person_sum=len(name_sheet)
    person_counter=0
    openCam = 0
    start_flag=0
    while (True):  # isOpened()  检测摄像头是否处于打开状态
        if(cv2.waitKey(1) & main.isActiveWindow() == False):
            break
        if(main.btn1_click % 2 == 1):
            #cap.open(video_ip)
            openCam = 1
            if start_flag==0:
                main.textBrowser.append("已经开始签到！")
                start_flag=1
            main.pushButton_1.setText("结束签到")
            ret, img = cap.read()  # 把摄像头获取的图像信息保存之img变量
            original_img=img
            if ret == True:  # 如果摄像头读取图像成功 #人脸检测：
                status, face_name_list, distance_min_list, face_box = face_recognition(img, face_features)
                # --
                if status == True:
                    # 画框
                    for i in range(len(face_name_list)):
                        cv2.rectangle(img, face_box[i]['left_top'], face_box[i]['right_bottom'], (255, 0, 0,), 2)
                        # 写文本
                        confidence = str(round(distance_min_list[i], 3))
                        print("confidence distnce:",confidence)
                        name_key = str(face_name_list[i])
                        if name_key== 'unknown':
                            Name_text = name_sheet[name_key]['name']
                            img_text = str(face_name_list[i]) + ' ' + confidence
                            font = cv2.FONT_HERSHEY_TRIPLEX
                            cv2.putText(img, img_text, face_box[i]['left_top'], font, 1, (0, 255, 0), 0)
                        else:
                            Name_text = name_key
                            img_text = str(face_name_list[i])
                            font = cv2.FONT_HERSHEY_TRIPLEX
                            cv2.putText(img, img_text, face_box[i]['left_top'], font, 1, (0, 255, 0), 0)
                        # 裁剪人脸：
                        y0 = face_box[i]['left_top'][1]
                        x0 = face_box[i]['left_top'][0]
                        y1 = face_box[i]['right_bottom'][1]
                        x1 = face_box[i]['right_bottom'][0]
                        face_img = original_img[y0:y1, x0:x1]
                        #做颜色转换
                        face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
                        if name_sheet[name_key]['check_in_status'] == False:
                            time_str = datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S')
                            name_sheet[name_key]['check_in_status'] = True
                            name_sheet[name_key]['Check_in_time']=time_str
                            stu_id=name_sheet[name_key]['id']
                            main.cardAdd(stu_id,Name_text, confidence, face_img)
                            msg="Check Log: "+time_str+"  "+name_sheet[name_key]['name']+"  签到成功！"
                            person_counter+=1
                            main.textBrowser.append(msg)

                scale = 1
                height = int(img.shape[0] * scale)
                width = int(img.shape[1] * scale)
                main.updateStreamSrc(cv2.resize(img, (width, height)))
        else:
            main.streamContainer.setPixmap(QtGui.QPixmap.fromImage(main.cameraBG))
            if (openCam == 1):
                openCam = 0

                time_str = datetime.datetime.strftime(datetime.datetime.now(), '%m-%d')

                main.textBrowser.append("结束签到！")
                msg="预计签到人数："+str(person_sum)
                main.textBrowser.append(msg)
                print(msg)

                msg="签到人数："+str(person_counter)
                main.textBrowser.append(msg)
                print(msg)

                msg="签到率："+str((round(person_counter/person_sum,2))*100)+"%"
                main.textBrowser.append(msg)
                print(msg)

                msg="结束签到，本窗口将在 15S 后自动关闭…………"
                main.textBrowser.append(msg)
                print(msg)
                time.sleep(15)


                excel_name = "..\\Check-Excel\\" + time_str + ".xlsx"
                name_sheet_pd=pd.DataFrame(name_sheet).T

                excel_postion = os.path.join(os.getcwd(), excel_name)
                msg = "签到名单已经导出至：" + excel_postion
                main.textBrowser.append(msg)
                print(msg)

                #释放摄像头资源
                cap.release()
                name_sheet_pd.to_excel(excel_name)

                break
    print("EXIT")
    sys.exit(0)

Video_Stram()







