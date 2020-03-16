
if __name__ == "__main__":
	with open('./data/in.bin','rb') as reader:
		bin1=reader.read()
	with open('./output/output.bin','rb') as reader:
		bin2=reader.read()
	count = 0;
	same = 0;
	while bin1 and bin2:
		if(bin1[0]==bin2[0]):
			same+=1
		count+=1
		bin1=bin1[1:]
		bin2=bin2[1:]

	while bin1:
		bin1=bin1[1:]
		count+=1
	print("正确率为：  ",same/count)
	

	
