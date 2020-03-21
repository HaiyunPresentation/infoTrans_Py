import numpy as np
import cv2
import struct
import CRC
from time import *

width = 73
inWidth = 41
locWidth = 16
border = 4

sLocWidth = 8
sblackWhite = 7

first = 0
end = 0


def getContours(image):
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	gray = cv2.blur(gray, (5, 5), 0)
	ret,gray=cv2.threshold(gray,127,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	contours,hierachy=cv2.findContours(gray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	#cv2.imwrite("out.png",gray)
	#cv2.drawContours(image,contours,-1,(0,0,255),3)
	#cv2.imwrite("output.png",gray)
	#cv2.waitKey()
	return contours,hierachy
	#cv2.drawContours(img,contours,-1,(0,0,255),3)
	#cv2.imwrite("output.png",img)

def computeRate1(contours,i,j):
	area1 = cv2.contourArea(contours[i])
	area2 = cv2.contourArea(contours[j])
	if area2 == 0:
		return False
	ratio = area1*1.0/area2
	if abs(ratio-49.0/25) < 1:
		#print(abs(ratio-49.0/25))
		return True
	return False

def computeRate2(contours,i,j):
	area1 = cv2.contourArea(contours[i])
	area2 = cv2.contourArea(contours[j])
	if area2 == 0:
		return False
	ratio = area1*1.0/area2
	if abs(ratio-25.0/9) < 1:
		#print(abs(ratio-25.0/9))
		return True
	return False

def getCenter(contours,i):
	M=cv2.moments(contours[i])
	x = (M['m10']/M['m00'])
	y = (M['m01']/M['m00'])
	return x,y

def detectContours(vec):
	distance1=np.sqrt((vec[0]-vec[2])**2+(vec[1]-vec[3])**2)
	distance2=np.sqrt((vec[0]-vec[4])**2+(vec[1]-vec[5])**2)
	distance3=np.sqrt((vec[2]-vec[4])**2+(vec[3]-vec[5])**2)
	if sum((distance1,distance2,distance3))/3<3:
		#print(sum((distance1,distance2,distance3))/3)
		return True
	return False

def judgeOrder(rec):
	if len(rec)<4:
		print(len(rec))
		print("not find enough diction point!")
		return -1,-1,-1,-1
	max = 0
	index = 0
	for i in range(len(rec)):
		if(rec[i][0]>max):
			max = rec[i][0]
			index = i
	for i in range(len(rec)):
		if i == index:
			continue
		for j in range(i+1,len(rec)):
			if j == index:
				continue
			for k in range(j+1,len(rec)):
				if k == index:
					continue
				distance1 = np.sqrt((rec[i][0] - rec[j][0]) ** 2 + (rec[i][1] - rec[j][1]) ** 2)
				distance2 = np.sqrt((rec[i][0] - rec[k][0]) ** 2 + (rec[i][1] - rec[k][1]) ** 2)
				distance3 = np.sqrt((rec[j][0] - rec[k][0]) ** 2 + (rec[j][1] - rec[k][1]) ** 2)
				if abs(np.square(distance1)+np.square(distance2)- np.square(distance3))/(2*distance1*distance2) < 0.1:
					if rec[j][0]<rec[k][0]:
						return i,j,index,k
					else:
						return i,k,index,j
				elif abs(np.square(distance1)+np.square(distance3)- np.square(distance2))/(2*distance1*distance3) < 0.1:
					if rec[i][0]<rec[k][0]:
						return j,i,index,k
					else:
						return j,k,index,i
				elif abs(np.square(distance2)+np.square(distance3)- np.square(distance1))/(2*distance2*distance3) < 0.1:
					if rec[i][0]<rec[j][0]:
						return k,i,index,j
					else:
						return k,j,index,i
	return -1,-1,-1,-1

def find(image,contours,hierachy,root=0):

	rec=[]
	for i in range(len(hierachy)):
		child = hierachy[i][2]
		grandchild = hierachy[child][2]
		if child!=-1 and grandchild !=-1:
			if computeRate1(contours,i,child) and computeRate2(contours,child,grandchild):
				x1,y1 = getCenter(contours,i)
				x2,y2 = getCenter(contours,child)
				x3,y3 = getCenter(contours,grandchild)
				if detectContours([x1,y1,x2,y2,x3,y3,i,child,grandchild]):
					rec.append([x1,y1,x2,y2,x3,y3,i,child,grandchild])
	if len(rec)<4:
		cv2.imwrite("wrong.png",image)
	i,j,k,t = judgeOrder(rec)
	if i==-1 or j==-1 or k ==-1 or t==-1:
		print("not find enough anchor point")
		return 

	vertexSrc = np.array([[rec[i][0],rec[i][1]],[rec[j][0],rec[j][1]],[rec[k][0],rec[k][1]],[rec[t][0],rec[t][1]]],dtype="float32")
	#print(vertexSrc)
	vertexWarp=np.array([[69.5,69.5],[69.5,659.5],[694.5,694.5],[659.5,69.5]],dtype="float32")
	M = cv2.getPerspectiveTransform(vertexSrc,vertexWarp)
	out = cv2.warpPerspective(image,M,(width*10,width*10))
	cv2.imwrite("wrong.png",out)
	return out

def demask(mat,row,col,count,thre):
	if(mat[row][col][count] > thre):
		mat[row][col][count] = 0
	else:
		mat[row][col][count] = 255

def decode(image,binstring):
	mat = np.full((width,width,3),0,dtype=np.float32)
	pwidth = 10
	i = 0
	for i in range(width*10):
		normali = i//pwidth
		for j in range(width*10):
			normalj = j//pwidth
			if(normali<len(mat) and normalj<len(mat)):
				#加权
				if i%10<3 or i%10>6 or j%10<3 or j%10>6:
					mat[normali][normalj][0]+=image[i][j][0]*0.2/84
					mat[normali][normalj][1]+=image[i][j][1]*0.2/84
					mat[normali][normalj][2]+=image[i][j][2]*0.2/84
				else:
					mat[normali][normalj][0]+=image[i][j][0]*0.05
					mat[normali][normalj][1]+=image[i][j][1]*0.05
					mat[normali][normalj][2]+=image[i][j][2]*0.05


	row=0
	thre = 110.0
	col=locWidth #
	count = 0;
	while row<width:
		if row<locWidth:
			if (row+col)% 2==0:
				demask(mat,row,col,count,thre)
			if mat[row][col][count] > thre:
				binstring+="0"
			else:
				binstring+="1"
			count+=1;
			if count>=3:
				count-=3
				col += 1
				if col>width-locWidth-1:
					if row!=locWidth-1:
						col = locWidth
					else:
						col = 0
					row += 1
		elif row<width-locWidth:
			if (row+col)% 2==0:
				demask(mat,row,col,count,thre)
			if mat[row][col][count] > thre:
				binstring+="0"
			else:
				binstring+="1"
			count+=1;
			if count>=3:
				count-=3
				col += 1
				if(col>width-1):
					if row !=width-locWidth-1:
						col = 0
					else:
						col = locWidth
					row += 1
		elif row < width-sLocWidth:
			if (row+col)% 2==0:
				demask(mat,row,col,count,thre)
			if mat[row][col][count] > thre:
				binstring+="0"
			else:
				binstring+="1"
			count+=1;
			if count>=3:
				count-=3
				col += 1
				if col>width-1:
					col = locWidth
					row += 1
		else:
			if (row+col)% 2==0:
				demask(mat,row,col,count,thre)
			if mat[row][col][count] > thre:
				binstring+="0"
			else:
				binstring+="1"
			count+=1;
			if count>=3:
				count-=3
				col += 1
				if col>width-sLocWidth-1:
					col = locWidth
					row += 1
	

	startOrEnd = 170
	startOrEndStr = ""
	for i in range(8):
		startOrEndStr += '{:08b}'.format(startOrEnd)
	global first
	global end

	if first==0 and binstring[:64]!=startOrEndStr:
		return 
	elif first ==0 and binstring[:64]==startOrEndStr:
		binstring=binstring[64:]
		first=1
	elif first ==1 and binstring[:64]==startOrEndStr:
		binstring=binstring[64:]
	elif first == 1 and binstring.find(startOrEndStr)!=-1 :
		if binstring[:64]!=startOrEndStr:
			binstring=binstring[:binstring.find(startOrEndStr)]
			end=1

	return binstring

def wirteResult(binstring):
	writer = open("./output/output.bin",'ab+')
	writerCheck = open("./output/valid.bin",'ab+')
	count = 0
	while len(binstring)>=11:
		if CRC.checkCRC(binstring[:11])==True:
			writerCheck.write(struct.pack('B', 255))
		else:
			writerCheck.write(struct.pack('B', 0))
			count+=1
			print("throw ",count)
		t = (int(binstring[:8],2))
		res = struct.pack('B', t)
		writer.write(res)
		binstring = binstring[11:]
	writer.close()
	return binstring

def checkStart(img):
	global first
#cv2.imwrite("problem.png",img)
	contours,hierachy = getContours(img)
	img=find(img,contours,np.squeeze(hierachy))
	binstring=""
	decode(img,binstring)
	return

def decodeFromVideo(filename):
	global end
	global first
	binstring = ""
	vc= cv2.VideoCapture(filename)
	if vc.isOpened():
		rval = True
	else:
		rval = False
	fps = 3
	k = 1
	count = 1
	record = 0
	while rval:
		rval,frame=vc.read()
		if frame is None:
			break
		if first == 0:
			print(k)
			checkStart(frame)
			if(first==1):
				record=k+1
		elif (k-record)%fps==0:
			print("Processing ",count," frame")
			contours,hierachy = getContours(frame)
			img=find(frame,contours,np.squeeze(hierachy))
			binstring = decode(img,binstring)
			binstring = wirteResult(binstring)
			count += 1
		#cv2.imwrite("./output/"+str(k)+".png",frame)
		k += 1
		if(end==1):
			break;
		#cv2.waitKey(1)
	vc.release()
	return

if __name__ == "__main__":
	#count = getGraph("./video/in.mp4")
	#count = getGraph("./video/in.MP4")
	#i = checkStart(cv2.imread("./output/16.png"))

	decodeFromVideo("./video/in.mp4")
	#first = 1
	#binstring = ""
	#img=cv2.imread("./output/17.png")
	#contours,hierachy = getContours(img)
	#img=find(img,contours,np.squeeze(hierachy))
	#binstring = decode(img,binstring)
	#wirteResult(binstring)

	#while i<count:
	#	img=cv2.imread("./output/"+str(i+1)+".png")
	#	contours,hierachy = getContours(img)
	#	img=find(img,contours,np.squeeze(hierachy))
	#	#cv2.imwrite("output.png",img)
	#	print(count-i)
	#	decode(img)
	#	if end == 1:
	#		break
	#	i+=3
