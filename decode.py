import numpy as np
from imutils.perspective import four_point_transform
import cv2

width = 72
inWidth = 40
locWidth = 16

def getContours(image):
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	#gray = cv2.blur(gray, (5, 5), 0)
	ret,gray=cv2.threshold(gray,100,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	contours,hierachy=cv2.findContours(gray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	cv2.imwrite("out.png",gray)
	cv2.waitKey()
	return gray,contours,hierachy
	#cv2.drawContours(img,contours,-1,(0,0,255),3)
	#cv2.imwrite("output.png",img)

def computeRate1(contours,i,j):
	area1 = cv2.contourArea(contours[i])
	area2 = cv2.contourArea(contours[j])
	if area2 == 0:
		return False
	ratio = area1*1.0/area2
	if abs(ratio-49.0/25) < 2:
		return True
	return False

def computeRate2(contours,i,j):
	area1 = cv2.contourArea(contours[i])
	area2 = cv2.contourArea(contours[j])
	if area2 == 0:
		return False
	ratio = area1*1.0/area2
	if abs(ratio-25.0/9) < 2:
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
					if abs(np.square(distance1)+np.square(distance2)- np.square(distance3))/(2*distance1*distance2) < 0.03:
						return i,j,k
				elif abs(distance1-distance3)/10<5:
					if abs(np.square(distance1)+np.square(distance3)- np.square(distance2))/(2*distance1*distance3) < 0.03:
						return i,j,k
				elif abs(distance2-distance3)/10<5:
					if abs(np.square(distance2)+np.square(distance3)- np.square(distance1))/(2*distance2*distance3) < 0.03:
						return i,j,k
	return -1,-1,-1

def find(image,contours,hierachy,root=0):
	rec=[]
	for i in range(len(hierachy)):
		child = hierachy[i][2]
		grandchild = hierachy[child][2]
		if child!=-1 and grandchild !=-1:
			if computeRate1(contours,i,child) and computeRate2(contours,child,grandchild):
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
	box = np.int32(box)

	#vertexWarp=np.array([[0,width*10],[0,0],[width*10,0],[width*10,width*10]],dtype="float32")
	#M = cv2.getPerspectiveTransform(box,vertexWarp)
	#out = cv2.warpPerspective(image,M,(width*10,width*10))

	rect = four_point_transform(image, box)
	out = cv2.resize(rect,(width*10,width*10))
	#box = cv2.boxPoints(rect)
	cv2.drawContours(image,[box],0,(0,0,255),2)
	cv2.imwrite("output.jpg",image)
	#out = image[box[1][0]:box[3][0],box[1][1]:box[3][1]]
	return out

def decode(image):
	mat = [[0.0 for i in range(width)]for j in range(width)]
	pwidth = 10
	i = 0
	for i in range(width*10):
		normali = i/pwidth
		for j in range(width*10):
			normalj = j/pwidth
			if(normali<len(mat) and normalj<len(mat)):
				#加权
				if i%10<3 or i%10>6 or j%10<3 or j%10>6:
					mat[int(normali)][int(normalj)]+=image[i][j]*0.2/84
				else:
					mat[int(normali)][int(normalj)]+=image[i][j]*0.05
				#if i%10==4 and j%10==4:
				#	mat[int(normali)][int(normalj)]=image[i][j]
	binstring=""
	#print(image[5][91])
	#print(mat[0][9])
	#转二进制
	row=0
	thre=127.5
	col=locWidth #
	while row<width:
		if row<locWidth:
			if mat[row][col] > thre:
				binstring+="0"
			else:
				binstring+="1"
			col += 1
			if col>width-locWidth-1:
				if row!=locWidth-1:
					col = locWidth
				else:
					col = 0
				row += 1
		elif row<width-locWidth:
			if mat[row][col] > thre:
				binstring+="0"
			else:
				binstring+="1"
			col += 1
			if(col>width-1):
				if row !=width-locWidth-1:
					col = 0
				else:
					col = locWidth
				row += 1
		else:
			if mat[row][col] > thre:
				binstring+="0"
			else:
				binstring+="1"
			col += 1
			if col>width-1:
				col = locWidth
				row += 1
	res=""
	#print(binstring)
	while binstring:
		t = (int(binstring[:8],2))
		res += chr(t)
		binstring = binstring[8:]
	print(res)
	return

if __name__ == "__main__":
	img=cv2.imread("test3.jpg")
	img,contours,hierachy = getContours(img)
	img=find(img,contours,np.squeeze(hierachy))
	cv2.imwrite("output.png",img)
	decode(img)