
import cv2

#cv2.namedWindow("camera", 1)
# 开启ip摄像头
#video = "http://admin:admin@192.168.31.136:8080"  # 此处@后的ipv4 地址需要改为app提供的地址
#video = "http://192.168.31.136:8080/video/mjpeg"
video = "rtsp://10.199.103.114:8080/video/h264"
cap = cv2.VideoCapture(video)

# ret, image_np = cap.read()
# print(type(image_np))


while True:
    # Start Camera, while true, camera will run

    ret, image_np = cap.read()

    print("image_np.shape",image_np.shape)
    # Set height and width of webcam
    scale=0.5
    height = int(image_np.shape[0]*scale)
    width = int(image_np.shape[1]*scale)

    # Set camera resolution and create a break function by pressing 'q'
    cv2.imshow('object detection', cv2.resize(image_np, (width, height)))
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break






