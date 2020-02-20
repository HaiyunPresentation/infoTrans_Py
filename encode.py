import cv2
import qrcode
from pyzbar import pyzbar
from PIL import Image
import os

def saveGraph(graphName,data):
	qr= qr = qrcode.QRCode(     
    version=3,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=2,
	)   #设置图片格式
	qr.add_data(data)
	qr.make(fit=False)
	img = qr.make_image()
	img.save(graphName+".png")

def encode(data):
	slice = 16
	length = len(data)
	num = 0#图片初始数量
	while length>slice:
		saveGraph(str(num),data[num*slice:num*slice+slice])
		length -= slice
		num += 1
	if length>0:
		saveGraph(str(num),data[num*slice:])
		num += 1
	fps=3#视频帧数
	size =(330,330)#需要转为视频的图片的尺寸
	video = cv2.VideoWriter("b.avi",cv2.VideoWriter_fourcc('M','J','P','G'),fps,size)

	for i in range(num):
		img=cv2.imread(str(i)+".png")
		video.write(img)



if __name__=="__main__":
	data = "公开信显示，近期，网络流传涉及该所若干谣言，如“新冠病毒源于人工合成”“病毒是从P4泄露的”“军方接管P4”“某研究人员因病毒泄露死亡”“某研究生是‘零号病人’”“某研究员实名举报所领导”等，引发了各界的持续关注，对该所科研人员造成极大的伤害，也严重干扰了该所承担的战“疫”应急科研攻关任务。\
据公开信，2019年12月30日至今，该所在病毒溯源、病原检测、药物筛选方面有诸多发现，比如1月5日即分离出病毒毒株，向世界卫生组织提交了病毒序列等。此外，该所还参与了新冠病毒肺炎病原学检测工作，自2020年1月26日起，累计检测疑似新冠肺炎病人咽拭子样本约4000份；派出由职工和研究生组成的小分队，支援黄冈市病原学检测等。\
公开信称，“回首过去一个多月的艰辛付出，我们问心无愧！”\
南都记者此前报道，武汉病毒研究所是专业从事病毒学基础研究及相关技术创新的综合性研究机构，拥有国内唯一的P4级生物安全实验室，有资质开展“高致病性的病原微生物实验”。2019年，该所的微生物菌（毒）种保藏中心被科技部、财政部指定为“国家病毒资源库”。"
	encode(data)
	
