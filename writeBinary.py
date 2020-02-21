import struct

if __name__=="__main__":
	with open ("data.txt",'r',encoding='UTF-8') as file:
		data=file.read()
	data="".join(data.split())
	data = data.encode("utf-8")
	wirter = open('in.bin','wb')
	wirter.write(data)
	wirter.close()
