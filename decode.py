import numpy as np
import cv2

def getContours(image):
	#转灰度图
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	#二值化
	ret,gray=cv2.threshold(gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	contours,hierachy=cv2.findContours(gray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	if result_detection:
		print('result',result_detection)
	return contours,hierachy
	#cv2.drawContours(img,contours,-1,(0,0,255),3)
	#cv2.imwrite("output.png",img)

def computeRate1(contours,i,j):
	area1 = cv2.contourArea(contours[i])
	area2 = cv2.contourArea(contours[j])
	if area2 == 0:
		return False
	ratio = area1*1.0/area2
	if abs(ratio-49.0/25)<1e-5:
		return True
	return False

def computeRate2(contours,i,j):
	area1 = cv2.contourArea(contours[i])
	area2 = cv2.contourArea(contours[j])
	if area2 == 0:
		return False
	ratio = area1*1.0/area2
	if abs(ratio-25.0/9)<1e-5:
		return True
	return False

def computeCenter(contours,i):
	M=cv2.moments(contours[i])#计算中心距
	x = int(M['m10']/M['m00'])
	y = int(M['m01']/M['m00'])
	return x,y

def detectContours(vec):
	distance1=np.sqrt((vec[0]-vec[2])**2+(vec[1]-vec[3])**2)
	distance2=np.sqrt((vec[0]-vec[4])**2+(vec[1]-vec[5])**2)
	distance3=np.sqrt((vec[2]-vec[4])**2+(vec[3]-vec[5])**2)
	if sum((distance1,distance2,distance3))/3<3:
		return True
	return False

def judgeAngle(rec):
	if len(rec)<3:
		print("not find enough diction point!")
		return -1,-1,-1
	for i in range(len(rec)):
		for j in range(i+1,len(rec)):
			for k in range(j+1,len(rec)):
				distance1 = np.sqrt((rec[i][0] - rec[j][0]) ** 2 + (rec[i][1] - rec[j][1]) ** 2)
				distance2 = np.sqrt((rec[i][0] - rec[k][0]) ** 2 + (rec[i][1] - rec[k][1]) ** 2)
				distance3 = np.sqrt((rec[j][0] - rec[k][0]) ** 2 + (rec[j][1] - rec[k][1]) ** 2)
				if abs(distance1-distance2)/10<5:
					if abs(np.square(distance1)+np.square(distance2)- np.square(distance3))/(2*distance1*distance2) < 0.02:
						return i,j,k
				elif abs(distance1-distance3)/10<5:
					if abs(np.square(distance1)+np.square(distance3)- np.square(distance2))/(2*distance1*distance3) < 0.02:
						return i,j,k
				elif abs(distance2-distance3)/10<5:
					if abs(np.square(distance2)+np.square(distance3)- np.square(distance1))/(2*distance2*distance3) < 0.02:
						return i,j,k
	return -1,-1,-1

def findDicPoint(image,contours,hierachy,root=0):
	rec=[]
	for i in range(len(hierachy)):
		child = hierachy[i][2]
		grandchild = hierachy[child][2]
		if child!=-1 and grandchild !=-1:
			if computeRate1(contours,i,child) and computeRate2(contours,child.grandchild):
				x1,y1 = computeCenter(contours,i)
				x2,y2 = computeCenter(contours,child)
				x3,y3 = computeCenter(contours,grandchild)
				if detectContours([x1,y1,x2,y2,x3,y3,i,child,grandchild]):
					rec.append([x1,y1,x2,y2,x3,y3,i,child,grandchild])
	i,j,k = judgeAngle(rec)
	if i==-1 or j==-1 or k ==-1:
		return
	ts = np.concatenate((contours[rec[i][6]],contours[rec[j][6]],contours[rec[k][6]]))
	rect = cv2.minAreaRect(ts)
	box = cv2.boxPoints(rect)

if __name__ == "__main__":
	img=cv2.imread("test.jpg")
	getContours(img)