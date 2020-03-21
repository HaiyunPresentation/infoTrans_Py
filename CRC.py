def xor(x, y):
    ret = []
    for i in range(1, len(y)):
        if x[i] == y[i]:
            ret.append('0')
        else:
            ret.append('1')
    return ''.join(ret)

def mod2div(x, y):
    size = len(y)
    tmp = x[0:size]
    while size < len(x):
        if tmp[0] == '1':
            tmp = xor(y, tmp) + x[size]
        else:
            tmp = xor('0'*size, tmp) + x[size]
        size += 1

    if tmp[0] == '1':
        tmp = xor(y, tmp)
    else:
        tmp = xor('0'*size, tmp)

    return tmp

def generateCRC(data, key):

    appended_data = data + '0'*(len(key)-1)
    remainder = mod2div(appended_data, key)

    return data + remainder

def getHightBit(num):
	res = 0
	while num:
		num=num>>1
		res+=1
	return res

def checkCRC(data):
	key='1011'

	keyLength = len(key)
	t = (int(data,2))
	div = (int(key,2))
	high=getHightBit(t)
	while high>keyLength-1:
		t = t^(div<<(high-keyLength))
		high = getHightBit(t)
	if(high==0):
		return True
	return False


if __name__=='__main__':
	tmp_input = 250
	print (tmp_input)

	data = '{:b}'.format(tmp_input)
	print (data)
	key = '1011'
	ans = encode(data, key)
	print (ans)
	crc = ans[-(len(key)-1):]
	print (crc)

	print(decode(ans,key))


'''
key = '1001'
f = open('text.txt','rb')
file_lines = (sum(1 for line in open('text.txt')))
f2 = open('t1.txt', 'a')
data = f.readline()
ans = encode(data, key)
print ans
crc = ans[-(len(key)-1):]
print crc
f2.write(data.rstrip() + ' ' + crc + '\n')
f2.write(data.rstrip() + ' ' + crc + '\n')
f.close()
f2.close()
'''