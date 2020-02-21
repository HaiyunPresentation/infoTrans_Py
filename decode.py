from pyzbar import pyzbar
from PIL import Image
import cv2

def getGraph(filename):
	vc= cv2.VideoCapture(filename)
	if vc.isOpened():
		rval,frame=vc.read()
		cv2.imwrite(str(0)+".jpg",frame)#第一帧
	else:
		rval=False
	fps = 1
	k = 1
	count = 1
	while rval:
		rval,frame=vc.read()
		if frame is None:
			break
		if(k%fps==0):#每隔fps帧数截取视频
			cv2.imwrite(str(count)+".jpg",frame)
			count += 1
		k += 1
		cv2.waitKey(1)
	vc.release()
	return count

def decode(filename):
	num = getGraph(filename)
	for i in range(num):
		text = pyzbar.decode(Image.open(str(i)+".jpg"))
		for texts in text:
			data = texts.data.decode('utf-8')
			print(data)
	return
if __name__=="__main__":
	decode("test.mp4")