import math
from  mtcnn.mtcnn import MTCNN
import numpy as np
from PIL import Image
import cv2
from numpy import asarray
#导包

detector = MTCNN()
def rotate(origin, point, angle, row):
    x1, y1 = point
    x2, y2 = origin
    y1 = row - y1
    y2 = row - y2
    angle = math.radians(angle)
    x = x2 + math.cos(angle) * (x1 - x2) - math.sin(angle) * (y1 - y2)
    y = y2 + math.sin(angle) * (x1 - x2) + math.cos(angle) * (y1 - y2)
    y = row - y
    return int(x), int(y)

def rotate_landmarks(landmarks, eye_center, angle, row):

    rotated_landmarks = dict()
    for facial_feature in landmarks.keys():
        landmark =landmarks[facial_feature]
        rotated_landmark = rotate(origin=eye_center, point=landmark, angle=angle, row=row)
        rotated_landmarks[facial_feature]=rotated_landmark
    return rotated_landmarks

def corp_face(image_array, landmarks,face_box):

    eye_landmark = np.concatenate([np.array(landmarks['left_eye']).reshape(1,2),
                                   np.array(landmarks['right_eye']).reshape(1,2)],axis=0)
    eye_center = np.mean(eye_landmark, axis=0).astype("int") #求人眼中心值

    mouth_landmark = np.concatenate([np.array(landmarks['mouth_left']).reshape(1,2),
                                   np.array(landmarks['mouth_right']).reshape(1,2)],axis=0)

    mouth_center = np.mean(mouth_landmark, axis=0).astype("int")
    mid_part = mouth_center[1] - eye_center[1]

    top_point = eye_center[1] - mid_part * 30 / 35
    bottom_point = mouth_center[1] + mid_part

    w = h = bottom_point - top_point #计算出切割的长和宽mouth_right

    x_min = min(landmarks['left_eye'][0]
                ,landmarks['right_eye'][0],landmarks['nose'][0],
                landmarks['mouth_left'][0],landmarks['mouth_right'][0])
    x_max = max( landmarks['left_eye'][0]
                ,landmarks['right_eye'][0], landmarks['nose'][0],
                landmarks['mouth_left'][0], landmarks['mouth_right'][0])

    x_center = (x_max - x_min) / 2 + x_min
    left, right = (x_center - w / 2, x_center + w / 2)
    pil_img = Image.fromarray(image_array)

    #整型转换
    left, top_point, right, bottom_point = [int(i) for i in [left, top_point, right, bottom_point]]
    #图片切割
    cropped_img = pil_img.crop((left, top_point, right, bottom_point))
    #转换成array对象

    return cropped_img


def align_face(face_base, face_box, landmarks):
    row=face_base.shape[0]
    rotate_angel = 0
    if landmarks['left_eye'][1]==landmarks['right_eye'][1]:#水平状态，不旋转
        return Image.fromarray(face_base[face_box['left_top'][1]:face_box['right_bottom'][1],
                               face_box['left_top'][0]:face_box['right_bottom'][0]])
    elif landmarks['left_eye'][0]==landmarks['right_eye'][0]:#垂直状态，必须旋转
        if landmarks['left_eye'][1]<landmarks['right_eye'][1]:
            rotate_angel = 90
        else:
            rotate_angel = - 90
    else:
        dy=(landmarks['right_eye'][1] - landmarks['left_eye'][1])
        dx= landmarks['right_eye'][0] - landmarks['left_eye'][0]
        k=dy/dx
        rotate_angel=math.atan(k)*180/math.pi
    print("rotate_angel:",rotate_angel)
    #求眼中点坐标
    center_x= (landmarks['right_eye'][0] + landmarks['left_eye'][0]) / 2
    center_y= (landmarks['right_eye'][1] + landmarks['left_eye'][1]) / 2
    eye_center=(center_x,center_y)

    rotate_matrix = cv2.getRotationMatrix2D(eye_center, rotate_angel, scale=1)
    rotated_img = cv2.warpAffine(face_base, rotate_matrix, (face_base.shape[1], face_base.shape[0]))
    # plt.figure()
    # plt.title("rotated_img")
    # plt.imshow(rotated_img)
    landmarks=rotate_landmarks(landmarks, eye_center, rotate_angel, row)
    #visualize_landmark(rotated_img, landmarks,"visualize_landmark_rotated_img")
    corp_img=corp_face(rotated_img,landmarks,face_box)
    # plt.figure()
    # plt.title("corp_img")
    # plt.imshow(corp_img)
    #img=Image.fromarray(corp_img)
    return corp_img

def face_tect(image, required_size=(160, 160)):

    faces_list=[]
    faces_box=[]
    pixels = asarray(image)

    # plt.figure()
    # plt.imshow(image)
    # detect faces in the image
    results = detector.detect_faces(pixels)
    # extract the bounding box from the first face
    if len(results)==0:
        return False,np.zeros(required_size),None
    else:
        for i in range(len(results)):
            x1, y1, width, height = results[i]['box']
            # bug fix
            x1, y1 = abs(x1), abs(y1)
            x2, y2 = x1 + width, y1 + height
            #人脸框的新坐标
            face_box={'left_top':(x1,y1),'right_bottom':(x2,y2)}
            #人的左右眼的新坐标
            landmarks=results[i]['keypoints']
            #visualize_landmark(pixels, landmarks,"visualize_landmark_pixels")
            image=align_face(pixels,face_box,landmarks)
            # resize pixels to the model size
            image = image.resize(required_size)
            face_array = asarray(image)
            faces_list.append(face_array)
            faces_box.append(face_box)
    faces_array=np.array(faces_list)
    return True ,faces_array,faces_box