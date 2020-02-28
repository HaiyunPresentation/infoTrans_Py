import cv2
import qrcode
from pyzbar import pyzbar
from PIL import Image
import os
import sys

def saveGraph(graphName,data):
	qr = qrcode.QRCode(     
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=0,
	)   #设置图片格式
	qr.add_data(data)
	qr.make(fit=False)
	img = qr.make_image()
	img.save("./video/"+graphName+".png")

def encode(data,outputFileName):
	slice = 5
	length = len(data)
	num = 0#图片初始数量
	while length>slice:
		saveGraph(str(num),data[num*slice:num*slice+slice])
		length -= slice
		num += 1
	if length>0:
		saveGraph(str(num),data[num*slice:])
		num += 1
	fps=15#视频帧数
	size =(370,370)#需要转为视频的图片的尺寸
	video = cv2.VideoWriter(outputFileName,cv2.VideoWriter_fourcc('M','J','P','G'),fps,size)

	for i in range(num):
		img=cv2.imread("./video/"+str(i)+".png")
		video.write(img)

def main(argv):
	inputFileName = "in.bin"
	outputFileName = "./video/in.avi"
	if len(argv)>1:
		inputFileName = argv[1]
		outputFileName = argv[2]
	reader = open(inputFileName,'rb')
	data=reader.read()
	data=data.decode('utf-8')
	encode(data,outputFileName)

if __name__=="__main__":
	main(sys.argv)
	
