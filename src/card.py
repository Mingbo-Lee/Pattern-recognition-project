from PyQt5 import QtCore, QtGui, QtWidgets
import cv2

class myCard(QtWidgets.QWidget):
    def __init__(self, number,name, conf, img, parent=None):
        super(myCard,self).__init__(parent)


        self.groupBox = QtWidgets.QGridLayout() 
        # self.groupBox.setGeometry(QtCore.QRect(211, 70))
        # self.groupBox.setMaximumSize(QtCore.QSize(1000, 70))
        self.groupBox.setObjectName("groupBox")

        #Cell------start
        self.label_number = QtWidgets.QLabel()
        # self.label_conf.setGeometry(QtCore.QRect(10, 44, 48, 16))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setBold(False)
        font.setWeight(50)
        self.label_number.setFont(font)
        self.label_number.setObjectName("label_number")
        self.label_number.setText("stu-id:")
        self.groupBox.addWidget(self.label_number)

        self.label_number_inp = QtWidgets.QLabel()
        # self.label_conf_inp.setGeometry(QtCore.QRect(64, 44, 54, 16))
        self.label_number_inp.setObjectName("label_number_inp")
        self.label_number_inp.setText(str(int(number)))
        self.groupBox.addWidget(self.label_number_inp)
        #cell--end


        #img-cell
        # rgbIcon = cv2.imread(img)
        img = cv2.resize(img, (80, 80))
        frame = QtGui.QImage(img, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)
        pix =  QtGui.QPixmap.fromImage(frame)
        self.item= QtWidgets.QGraphicsPixmapItem(pix)
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.addItem(self.item)

        self.face_pic = QtWidgets.QGraphicsView()
        # self.face_pic.setGeometry(QtCore.QRect(0, 0, 41, 38))
        self.face_pic.setFixedSize(100,100)
        self.face_pic.setObjectName("face_pic")
        self.face_pic.setScene(self.scene)
        self.groupBox.addWidget(self.face_pic)
        #--img-cell


        self.label_name = QtWidgets.QLabel()
        # self.label_name.setGeometry(QtCore.QRect(10, 22, 36, 16))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setBold(False)
        font.setWeight(50)
        self.label_name.setFont(font)
        self.label_name.setObjectName("label_name")
        self.label_name.setText("姓名：")
        self.groupBox.addWidget(self.label_name)


        self.label_name_inp = QtWidgets.QLabel()
        # self.label_name_inp.setGeometry(QtCore.QRect(64, 22, 54, 16))
        self.label_name_inp.setObjectName("label_name_inp")
        self.label_name_inp.setText(name)
        self.groupBox.addWidget(self.label_name_inp)
        

        #Cell------start
        self.label_conf = QtWidgets.QLabel()
        # self.label_conf.setGeometry(QtCore.QRect(10, 44, 48, 16))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setBold(False)
        font.setWeight(50)
        self.label_conf.setFont(font)
        self.label_conf.setObjectName("label_conf")
        self.label_conf.setText("置信距离：")
        self.groupBox.addWidget(self.label_conf)

        self.label_conf_inp = QtWidgets.QLabel()
        # self.label_conf_inp.setGeometry(QtCore.QRect(64, 44, 54, 16))
        self.label_conf_inp.setObjectName("label_conf_inp")
        self.label_conf_inp.setText(conf)
        self.groupBox.addWidget(self.label_conf_inp)
        #cell--end



        self.setLayout(self.groupBox)


    #     # self.retranslateUi()
    #     # QtCore.QMetaObject.connectSlotsByName(Form)

    # def retranslateUi(self, Form):
    #     _translate = QtCore.QCoreApplication.translate
    #     Form.setWindowTitle(_translate("Form", "Form"))
    #     self.groupBox.setTitle(_translate("Form", "GroupBox"))
    #     self.label_name.setText(_translate("Form", "姓名："))
    #     self.label_name_inp.setText(_translate("Form", "TextLabel"))
    #     self.label_conf.setText(_translate("Form", "置信度："))
    #     self.label_conf_inp.setText(_translate("Form", "TextLabel"))
