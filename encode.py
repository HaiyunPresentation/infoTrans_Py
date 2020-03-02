import cv2
import numpy as np
from PIL import Image,ImageDraw

border = 4
width = 80
inWidth = 40
locWidth = 16
blackWhite = 14

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
	for i in range(border+4,border+4+6):
		for j in range(border+4,border+4+6):
			mat[i][j] = 0
			mat[i][width-j-1] = 0
			mat[width-j-1][i] = 0
	return

def encode(mat,data):
	binstring=""
	#转二进制
	for ch in data:
		binstring += '{:08b}'.format(ord(ch.encode('utf-8')))
	row=border #记录绘制到第几行
	col=border + locWidth #
	while binstring:
		if row<border+locWidth:
			if int(binstring[0]) == 1:
				mat[row][col] = 0
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
			col += 1
			if col>width-border-1:
				if row != width-border-locWidth-1:
					col = border
				else:
					col = border + locWidth
				row += 1
			binstring=binstring[1:]
		else:
			if int(binstring[0]) == 1:
				mat[row][col] = 0
			col += 1
			if col>width-border-1:
				col = border + locWidth
				row += 1
			binstring=binstring[1:]
	print(row)
	#print(bitstring)
	#res=""
	#while bitstring:
	#	t = (int(bitstring[:8],2))
	#	res += chr(t)
	#	bitstring = bitstring[8:]
	#print(res)
	return

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
	cv2.imwrite("test.png",img)
	cv2.waitKey()
	return
if __name__=="__main__":
	#mat=np.zeros((120,120),dtype = np.uint8)
	mat = [[255 for i in range(width)]for j in range(width)]
	drawLocPoint(mat)
	#genImage(mat,width*10,1)
	encode(mat,"hello world asldjk aslkdjzcm asldkjalks lkasjdl kajlqw oqw joqj qwj lajd laj laksdm alsjdlaskjdqp ppqwopejqwpoejqpwjepqjalskdjalksjdclzxcn,zvnajkfjaldaskdlaskjdlkxzcnzvmladjf;akf;asclksjfka;jdfldaksjwoiejflskfjklsjfijzcmlksjfaijflasknaljwijh jalsj laj j w lakdlasknd;aa  55555555555555555555555555555555555555555555555555555555555555")
	genImage(mat,width*10,1)