import cv2
import numpy as np
import struct
import os
import sys
import zlib
import CRC
from time import *
border = 4
width = 81
inWidth = 41
locWidth = 16
blackWhite = 14

sLocWidth = 8
sblackWhite = 7

def drawLocPoint(mat):
	#创建定位点
	for i in range(border,border+blackWhite):
		#左上角
		mat[i][border] = 0		#竖
		mat[i][border+blackWhite-1] = 0
		mat[i][border+1] = 0		
		mat[i][border+blackWhite-1-1] = 0
		mat[border][i] = 0		#横
		mat[border+blackWhite-1][i] = 0
		mat[border+1][i] = 0		#横
		mat[border+blackWhite-1-1][i] = 0
		#左下角
		mat[width-border-blackWhite][i] = 0
		mat[width-border-1][i] = 0
		mat[width-border-blackWhite+1][i] = 0
		mat[width-border-1-1][i] = 0
		mat[width-i-1][border] = 0
		mat[width-i-1][border+blackWhite-1] = 0
		mat[width-i-1][border+1] = 0
		mat[width-i-1][border+blackWhite-1-1] = 0
		#右上角和左上角对称
		mat[i][width-border-blackWhite] = 0
		mat[i][width-border-1] = 0
		mat[i][width-border-blackWhite+1] = 0
		mat[i][width-border-1-1] = 0
		mat[border][width-i-1] = 0
		mat[border+blackWhite-1][width-i-1] = 0
		mat[border+1][width-i-1] = 0
		mat[border+blackWhite-1-1][width-i-1] = 0
	for i in range(border,border+sblackWhite):
		#右下角
		mat[width-i-1][width-border-1] = 0		#竖
		mat[width-i-1][width-(border+sblackWhite)] = 0
		mat[width-border-1][width-i-1] = 0		#横
		mat[width-(border+sblackWhite)][width-i-1] = 0

	for i in range(border+4,border+4+6):
		for j in range(border+4,border+4+6):
			mat[i][j] = 0
			mat[i][width-j-1] = 0
			mat[width-j-1][i] = 0

	for i in range(border+2,border+2+3):
		for j in range(border+2,border+2+3):
			mat[width-i-1][width-j-1] = 0
	return

def mask(mat,row,col,count):
	if(mat[row][col][count]==255):
		mat[row][col][count] = 0
	else:
		mat[row][col][count] = 255
	return
def encode(mat,binstring):
	row=border #记录绘制到第几行
	col=border + locWidth #记录绘制到第几列
	count = 0#rgb通道变换
	while binstring and row < width - border:
		if row<border+locWidth:
			if int(binstring[0]) == 1:
				mat[row][col][count] = 0
			else:
				mat[row][col][count] = 255
			if (col+row)% 2==0:
				mask(mat,row,col,count)
			count+=1
			if count>=3:
				count-=3
				col += 1
				if col>width-border-locWidth-1:
					if row!=border+locWidth-1 :
						col = border + locWidth
					else:
						col = border
					row += 1
			binstring=binstring[1:]
		elif row<width-border-locWidth:
			if int(binstring[0]) == 1:
				mat[row][col][count] = 0
			else:
				mat[row][col][count] = 255
			if (col+row)% 2==0:
				mask(mat,row,col,count)
			count+=1
			if count>=3:
				count-=3
				col += 1
				if col>width-border-1:
					if row != width-border-locWidth-1:
						col = border
					else:
						col = border + locWidth
					row += 1
			binstring=binstring[1:]
		elif row < width-border-sLocWidth:
			if int(binstring[0]) == 1:
				mat[row][col][count] = 0
			else:
				mat[row][col][count] = 255
			if (col+row)% 2==0:
				mask(mat,row,col,count)
			count+=1
			if count>=3:
				count-=3
				col += 1
				if col>width-border-1:
					col = border + locWidth
					row += 1
			binstring=binstring[1:]
		else:
			if int(binstring[0]) == 1:
				mat[row][col][count] = 0
			else:
				mat[row][col][count] = 255
			if (col+row)% 2==0:
				mask(mat,row,col,count)
			count+=1
			if count>=3:
				count-=3
				col += 1
				if col>width-sLocWidth-border-1:
					col = border + locWidth
					row += 1
			binstring=binstring[1:]
	#print(row)
	#print(bitstring)
	#res=""
	#while bitstring:
	#	t = (int(bitstring[:8],2))
	#	res += chr(t)
	#	bitstring = bitstring[8:]
	#print(res)
	return binstring

def drawPoint():
	return

def genImage(mat,width,filename):
	#begin_time = time()
	img = np.zeros((width,width,3),dtype=np.uint8)
	pwidth = 10
	for i in range(width):
		normali = i//pwidth
		for j in range(width):
			normalj = j//pwidth
			if(normali<len(mat) and normalj<len(mat)):
				img[i][j][0]=(mat[normali][normalj][0])
				img[i][j][1]=(mat[normali][normalj][1])
				img[i][j][2]=(mat[normali][normalj][2])
				#img[i][j][0]=int(mat[int(normali)][int(normalj)][0])
				#img[i][j][1]=int(mat[int(normali)][int(normalj)][1])
				#img[i][j][2]=int(mat[int(normali)][int(normalj)][2])
	#end_time = time()
	#run_time = end_time-begin_time
	#print ('该循环程序运行时间：',run_time)
	cv2.imwrite(filename,img)
	return

def imgToVideo(outputFileName,num):
	fps=10#视频帧数
	size =(width*10,width*10)#需要转为视频的图片的尺寸
	video = cv2.VideoWriter(outputFileName,cv2.VideoWriter_fourcc('M','J','P','G'),fps,size)

	for i in range(num):
		img=cv2.imread("./video/"+str(i)+".png")
		video.write(img)
def genBlankFrame():
	mat = np.full((width,width,3),255,dtype=np.uint8)
	drawLocPoint(mat)
	genImage(mat,width*10,"./video/"+str(0)+".png")

def main(argv):
	#mat=np.zeros((120,120),dtype = np.uint8)
	#genImage(mat,width*10,1)
	inputFileName = "./data/in.bin"
	outputFileName = "./video/in.avi"
	if len(argv)>1:
		inputFileName = argv[1]
		outputFileName = argv[2]
	with open(inputFileName,'rb') as reader:
		data=reader.read()
	#data = ("Gettysburg Address"
	#		"Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal. "
	#		"Now we are engaged in a great civil war, testing whether that nation, or any nation so conceived and so dedicated, can long endure. We are met on a great battle-field of that war. We have come to dedicate a portion of that field, as a final resting place for those who here gave their lives that that nation might live. It is altogether fitting and proper that we should do this. "
	#		"But, in a larger sense, we can not dedicate -- we can not consecrate -- we can not hallow -- this ground. The brave men, living and dead, who struggled here, have consecrated it, far above our poor power to add or detract. The world will little note, nor long remember what we say here, but it can never forget what they did here. It is for us the living, rather, to be dedicated here to the unfinished work which they who fought here have thus far so nobly advanced. It is rather for us to be here dedicated to the great task remaining before us -- that from these honored dead we take increased devotion to that cause for which they gave the last full measure of devotion -- that we here highly resolve that these dead shall not have died in vain -- that this nation, under God, shall have a new birth of freedom -- and that government of the people, by the people, for the people, shall not perish from the earth."
	#		"Abraham Lincoln"
	#		"November 19, 1863")
	
	binstring=""
	key = '1011'
	#begin_time = time()
	for ch in data:
		#print(struct.unpack('B',ch))
		binstring += CRC.generateCRC('{:08b}'.format(ch),key)
	#end_time = time()
	#run_time = end_time-begin_time
	#print ('该循环程序运行时间：',run_time)
	startOrEnd = 170
	startOrEndStr = ""
	for i in range(8):
		startOrEndStr += '{:08b}'.format(startOrEnd)
	binstring = startOrEndStr + binstring
	binstring = binstring + startOrEndStr

	genBlankFrame()
	num = 1

	while(binstring):
		#mat = np.zeros([width, width, 3], np.uint8)
		mat = np.full((width,width,3),255,dtype=np.uint8)
		#mat = [[255 for i in range(width)]for j in range(width)]
		drawLocPoint(mat)
		#begin_time = time()
		binstring=encode(mat,binstring)
		genImage(mat,width*10,"./video/"+str(num)+".png")
		#end_time = time()
		#run_time = end_time-begin_time
		#print ('该循环程序运行时间：',run_time)
		num+=1
		print(len(binstring))
	imgToVideo("./video/in.avi",num)

if __name__=="__main__":
	main(sys.argv)
	#num = 165
	#imgToVideo("./video/in.avi",num)