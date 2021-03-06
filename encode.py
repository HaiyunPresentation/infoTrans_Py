import cv2
import numpy as np
import os
import sys
border = 4
width = 80
inWidth = 40
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

def mask(mat,row,col):
	if(mat[row][col]==255):
		mat[row][col] = 0
	else:
		mat[row][col] = 255
def encode(mat,binstring):
	row=border #记录绘制到第几行
	col=border + locWidth #
	while binstring and row < width - border:
		if row<border+locWidth:
			if int(binstring[0]) == 1:
				mat[row][col] = 0
			if (col+row)% 2==0:
				mask(mat,row,col)
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
				mat[row][col] = 0
			if (col+row)% 2==0:
				mask(mat,row,col)
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
				mat[row][col] = 0
			if (col+row)% 2==0:
				mask(mat,row,col)
			col += 1
			if col>width-border-1:
				col = border + locWidth
				row += 1
			binstring=binstring[1:]
		else:
			if int(binstring[0]) == 1:
				mat[row][col] = 0
			if (col+row)% 2==0:
				mask(mat,row,col)
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
	img = np.zeros((width,width,1),dtype=np.uint8)
	pwidth = width/len(mat)#pwidth一般取10
	for i in range(width):
		normali = i/pwidth
		for j in range(width):
			normalj = j/pwidth
			if(normali<len(mat) and normalj<len(mat)):
				img[i][j][0]=int(mat[int(normali)][int(normalj)])
	cv2.imwrite(filename,img)
	return

def imgToVideo(outputFileName,num):
	fps=20#视频帧数
	size =(width*10,width*10)#需要转为视频的图片的尺寸
	video = cv2.VideoWriter(outputFileName,cv2.VideoWriter_fourcc('M','J','P','G'),fps,size)

	for i in range(num):
		img=cv2.imread("./video/"+str(i)+".png")
		video.write(img)

def main(argv):
	#mat=np.zeros((120,120),dtype = np.uint8)
	#genImage(mat,width*10,1)
	inputFileName = "./data/in.bin"
	outputFileName = "./video/in.avi"
	if len(argv)>1:
		inputFileName = argv[1]
		outputFileName = argv[2]
	with open(inputFileName,'rb') as reader:
		data=reader.read().decode('utf-8')
	#data = ("Gettysburg Address"
	#		"Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal. "
	#		"Now we are engaged in a great civil war, testing whether that nation, or any nation so conceived and so dedicated, can long endure. We are met on a great battle-field of that war. We have come to dedicate a portion of that field, as a final resting place for those who here gave their lives that that nation might live. It is altogether fitting and proper that we should do this. "
	#		"But, in a larger sense, we can not dedicate -- we can not consecrate -- we can not hallow -- this ground. The brave men, living and dead, who struggled here, have consecrated it, far above our poor power to add or detract. The world will little note, nor long remember what we say here, but it can never forget what they did here. It is for us the living, rather, to be dedicated here to the unfinished work which they who fought here have thus far so nobly advanced. It is rather for us to be here dedicated to the great task remaining before us -- that from these honored dead we take increased devotion to that cause for which they gave the last full measure of devotion -- that we here highly resolve that these dead shall not have died in vain -- that this nation, under God, shall have a new birth of freedom -- and that government of the people, by the people, for the people, shall not perish from the earth."
	#		"Abraham Lincoln"
	#		"November 19, 1863")
	binstring=""
	#转二进制
	for ch in data:
		binstring += '{:08b}'.format(ord(ch.encode('utf-8')))

	num = 0
	while(binstring):
		mat = [[255 for i in range(width)]for j in range(width)]
		drawLocPoint(mat)
		binstring=encode(mat,binstring)
		genImage(mat,width*10,"./video/"+str(num)+".png")
		num+=1
		print(len(binstring))
	imgToVideo("./video/in.avi",num)

if __name__=="__main__":
	#main(sys.argv)
	num = 165
	imgToVideo("./video/in.avi",num)