import numpy as np
import cv2

width = 72
inWidth = 40
locWidth = 16
border = 4

sLocWidth = 8
sblackWhite = 7

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
	if abs(ratio-49.0/25) < 1:
		return True
	return False

def computeRate2(contours,i,j):
	area1 = cv2.contourArea(contours[i])
	area2 = cv2.contourArea(contours[j])
	if area2 == 0:
		return False
	ratio = area1*1.0/area2
	if abs(ratio-25.0/9) < 1:
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
	if sum((distance1,distance2,distance3))/3<1:
		return True
	return False

def judgeOrder(rec):
	if len(rec)<4:
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
				if abs(distance1-distance2)/10<5:
					if abs(np.square(distance1)+np.square(distance2)- np.square(distance3))/(2*distance1*distance2) < 0.1:
						if rec[j][0]<rec[k][0]:
							return i,j,index,k
						else:
							return i,k,index,j
				elif abs(distance1-distance3)/10<5:
					if abs(np.square(distance1)+np.square(distance3)- np.square(distance2))/(2*distance1*distance3) < 0.1:
						if rec[i][0]<rec[k][0]:
							return j,i,index,k
						else:
							return j,k,index,i
				elif abs(distance2-distance3)/10<5:
					if abs(np.square(distance2)+np.square(distance3)- np.square(distance1))/(2*distance2*distance3) < 0.1:
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
	i,j,k,t = judgeOrder(rec)
	if i==-1 or j==-1 or k ==-1 or t==-1:
		print("not find enough anchor point")
		return 

	#ts = np.concatenate((contours[rec[i][6]],contours[rec[j][6]],contours[rec[k][6]]))
	#rect = cv2.minAreaRect(ts)
	#box = cv2.boxPoints(rect)
	#box = np.int32(box)
	vertexSrc = np.array([[rec[i][0],rec[i][1]],[rec[j][0],rec[j][1]],[rec[k][0],rec[k][1]],[rec[t][0],rec[t][1]]],dtype="float32")
	#print(vertexSrc)
	vertexWarp=np.array([[69.5,69.5],[69.5,649.5],[684.5,684.5],[649.5,69.5]],dtype="float32")
	M = cv2.getPerspectiveTransform(vertexSrc,vertexWarp)
	out = cv2.warpPerspective(image,M,(width*10,width*10))

	#rect = four_point_transform(image, box)
	#out = cv2.resize(rect,(width*10,width*10))
	#box = cv2.boxPoints(rect)
	#cv2.drawContours(image,[box],0,(0,0,255),2)
	#cv2.imwrite("output.jpg",image)
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
			if (row+col)% 2==0:
				if(mat[row][col] > thre):
					mat[row][col] = 0
				else:
					mat[row][col] = 255
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
			if (row+col)% 2==0:
				if(mat[row][col] > thre):
					mat[row][col] = 0
				else:
					mat[row][col] = 255
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
		elif row < width-sLocWidth:
			if (row+col)% 2==0:
				if(mat[row][col] > thre):
					mat[row][col] = 0
				else:
					mat[row][col] = 255
			if mat[row][col] > thre:
				binstring+="0"
			else:
				binstring+="1"
			col += 1
			if col>width-1:
				col = locWidth
				row += 1
		else:
			if (row+col)% 2==0:
				if(mat[row][col] > thre):
					mat[row][col] = 0
				else:
					mat[row][col] = 255
			if mat[row][col] > thre:
				binstring+="0"
			else:
				binstring+="1"
			col += 1
			if col>width-sLocWidth-1:
				col = locWidth
				row += 1
	res=""
	#print(binstring)
	while binstring:
		t = (int(binstring[:8],2))
		res += chr(t)
		binstring = binstring[8:]
	with open("./output/output.txt",'a+') as writer:
		writer.write(res)
	return

def getGraph(filename):
	vc= cv2.VideoCapture(filename)
	if vc.isOpened():
		rval,frame=vc.read()
		cv2.imwrite("./output/"+str(0)+".png",frame)#第一帧
	else:
		rval=False
	fps = 3
	k = 1
	count = 1
	while rval:
		rval,frame=vc.read()
		if frame is None:
			break
		if(k%fps==0):
			cv2.imwrite("./output/"+str(count)+".png",frame)
			count += 1
		k += 1
		#cv2.waitKey(1)
	vc.release()
	return count

if __name__ == "__main__":
	#count = getGraph("./video/in.mp4")
	count=188
	i = 13
	while i<count:
		img=cv2.imread("./output/"+str(i)+".png")
		img,contours,hierachy = getContours(img)
		img=find(img,contours,np.squeeze(hierachy))
		cv2.imwrite("output.png",img)
		print(count-i)
		decode(img)
		i+=1