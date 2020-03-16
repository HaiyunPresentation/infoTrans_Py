import struct
import random
import string

if __name__=="__main__":
	with open ("./data/data.txt",'rb') as file:
		data=file.read()
	#data="".join(data.split())
	#data= ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(90000))
	with open('./data/in.bin','wb') as writer:
		writer.write(data)
