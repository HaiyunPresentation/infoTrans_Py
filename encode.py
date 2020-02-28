import cv2
import numpy as np
from PIL import Image,ImageDraw

border = 4
width = 96
inWidth = 72
locWidth = 8

def drawLocPoint(mat):
	#创建定位点
	for i in range(border,border+7):
		#左上角
		mat[i][border] = 0		#横
		mat[i][border+7-1] = 0
		mat[border][i] = 0		#竖
		mat[border+7-1][i] = 0
		#左下角
		mat[width-border-7][i] = 0
		mat[width-border-1][i] = 0
		mat[width-i-1][border] = 0
		mat[width-i-1][border+7-1] = 0
		#右上角和左上角对称
		mat[i][width-border-7] = 0
		mat[i][width-border-1] = 0
		mat[border][width-i-1] = 0
		mat[border+7-1][width-i-1] = 0
	for i in range(border+2,border+2+3):
		for j in range(border+2,border+2+3):
			mat[i][j] = 0
			mat[i][width-j-1] = 0
			mat[width-j-1][i] = 0
	return

def encode(mat,data):
	bitstring=""
	#转二进制
	for ch in data:
		bitstring += '{:08b}'.format(ord(ch.encode('utf-8')))
	row=border #记录绘制到第几行
	col=border + locWidth #
	while bitstring:
		if row<border+locWidth:
			if int(bitstring[0]) == 1:
				mat[row][col] = 0
			col += 1
			if(col>width-border-locWidth-1):
				col = border + locWidth
				row += 1
			bitstring=bitstring[1:]
		elif row<width-border-locWidth:
			if int(bitstring[0]) == 1:
				mat[row][col] = 0
			col += 1
			if(col>width-border-1):
				col = border
				row += 1
			bitstring=bitstring[1:]
		else:
			if int(bitstring[0]) == 1:
				mat[row][col] = 0
			col += 1
			if(col>width-border-locWidth-1):
				col = border + locWidth
				row += 1
			bitstring=bitstring[1:]
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
	encode(mat,"hello worlsxxxcvnnweiuroiwu982374983274981ihsdojfs6x15x1v6x1v31x31sd6fsfsfd what's your name ? salkjdlkasjdla    s x z   x cn , c n x m z m n, a  . . . z / . a;  al s d ; qw ' a  s'd[q]q-e=q-=-asdasldasd.zmc.zm.,asmd;aasdasdmcn,zcn,mzcn,mzc,mxaskldjasldasdas m,n,aslaskldjqlwjoisjclkznajdlkasjdlkasjdlkzcm,znv,mnalksdjlaskjdksc,mzvcn,manflkasjfdlkascz,cnxcnlasjdlasjdlkashhhhhhhhhhhhhhh1212346456789")
	genImage(mat,width*10,1)