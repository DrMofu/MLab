'''
M小白实验室
#1 玩转labo
作者：M小白
'''
import time
from PIL import ImageGrab
import numpy as np
import re
import autopy
import win32api
import win32con

SLEEP_TIME = 0.5 # 刷新间隔


def getScreen(startX,startY,endX,endY):	
	img = ImageGrab.grab((startX,startY,endX,endY)) 
	# 转为灰度图
	img = img.convert('L')  
	# 转化为array
	imgArray = np.array(img)/255
	return imgArray

def getCode(imgArray):
	imgY,imgX = imgArray.shape
	totalAera = 4   # 划分几个区域识别 这里设置4个  图像横向切开 4个区域纵向排列
	aera = [0]*totalAera  # 初始化区域列表
	# 确定各个区域的明暗程度
	stepY = int(imgY/totalAera)
	uncodeKey = []  # 非编码
	codekey = 0	 # 编码
	for i in range(totalAera):
		aera[i] = imgArray[stepY*i:stepY*(i+1)].mean()
		if aera[i]>0.5:
			codekey += 2**i
			# print("第%s个区域是白色，亮度为%s" % (i+1,aera[i]))
			uncodeKey.append(str(i+1))
		else:
			pass
			# print("第%s个区域是黑色，亮度为%s" % (i+1,aera[i]))

	# print("\n编码情况下 按下的键的编号为%s" % codekey)
	# print("\n非编码下 按下的键的编号为%s" % (" ".join(uncodeKey)))
	return codekey,uncodeKey

def changeHtml(codekey):
	with open('./index.html','r',encoding='UTF-8') as f:
		string = f.read()
		
	# print("修改前：")
	# print(string)
	# print("\n修改后：")
	stringNew = re.sub(';">(.*)</p>',';">%s</p>' % codekey,string)
	# print(stringNew)

	with open('./index.html','w',encoding='UTF-8') as f:
		f.write(stringNew)

def simulateKey(codekey):
	keyEvent = [87,83,65,68,37,39,88,13] # W S A D 左方向键 右方向键 X 回车
	keyValue = ['W','S','A','D','<-','->','X','回车']
	if codekey>0 and codekey<=8:
		win32api.keybd_event(keyEvent[codekey-1],0,0,0)
		print(keyValue[codekey-1])

def main():
	count = 0
	while(1):
		# 1 截屏
		imgArray = getScreen(956, 100, 1374, 600)	
		# 2. 获取图片中指定N个区域的明亮程度与编码
		codekey,uncodeKey = getCode(imgArray)

		# 3. 将获取的内容输入到html文件中（用于展示中间结果）
		changeHtml(codekey)

		# 4. 键盘鼠标模拟
		simulateKey(codekey)
		
		count += 1
		print(codekey)
		time.sleep(SLEEP_TIME)

if __name__ == '__main__':
	main()