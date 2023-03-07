import os
import cv2
import numpy as np
from PIL import Image
# import scipy.io
import torch
from torch.utils import data
import random
# from cStringIO import StringIO


# def load_image_with_cache(path, cache=None, lock=None):
# 	if cache is not None:
# 		if not cache.has_key(path):
# 			with open(path, 'rb') as f:
# 				cache[path] = f.read()
# 		return Image.open(StringIO(cache[path]))
# 	return Image.open(path)


class Data(data.Dataset):
	def __init__(self, root, lst,yita=0.5,
		mean_bgr = np.array([104.00699, 116.66877, 122.67892]),
		crop_size=None, rgb=True, scale=None):
		self.mean_bgr = mean_bgr
		self.root = root
		self.lst = lst
		self.yita = yita
		self.crop_size = crop_size
		self.rgb = rgb
		self.scale = scale
		self.cache = {}

		lst_dir = os.path.join(self.root, self.lst)
		self.files = np.loadtxt(lst_dir, dtype=str)
		with open(lst_dir, 'r') as f:
			self.files = f.readlines()
			self.files = [line.strip() for line in self.files]
		# print(self.files)
		# self.files = os.listdir(root)

	def __len__(self):
		return len(self.files)

	def __getitem__(self, index):
		# print(self.files)
		data_file = self.files[index]
		# print(data_file)
		# load Image
		img_file = data_file
		print(img_file)
		# print(img_file)
		if not os.path.exists(img_file):
			img_file = img_file.replace('jpg', 'png')
		img = Image.open(img_file)
		# img = load_image_with_cache(img_file, self.cache)
		# load gt image
		# gt_file = self.root + data_file[1]
		# gt = Image.open(gt_file)
		# gt = load_image_with_cache(gt_file, self.cache)
		# if gt.mode == '1':
		# 	gt  = gt.convert('L')

		return (self.transform(img),self.top,self.bottom,self.left,self.right,self.old_h,self.old_w)

	def transform(self, img):
		img = img.convert("RGB")
		# gt = np.array(gt, dtype=np.float32)
		# if len(gt.shape) == 3:
		# 	gt = gt[:, :, 0]
		# gt /= 255.
		# gt[gt >= self.yita] = 1
		# gt = torch.from_numpy(np.array([gt])).float()
		img = np.array(img, dtype=np.float32)
		print(img.shape)
		if self.rgb:
			img = img[:, :, ::-1]  # RGB->BGR
		img -= self.mean_bgr
		data = []
		if self.scale is not None:
			for scl in self.scale:
				img_scale = cv2.resize(img, dsize=(352, 352), fx=scl, fy=scl, interpolation=cv2.INTER_LINEAR)
				data.append(torch.from_numpy(img_scale.transpose((2, 0, 1))).float())
			return data

		img_information = resize_keep_ratio(img,(720,1280))
		img = img_information[0]
		self.top = img_information[1]
		self.bottom = img_information[2]
		self.left = img_information[3]
		self.right = img_information[4]
		self.old_w = img_information[5]
		self.old_h = img_information[6]
		img = img.transpose((2, 0, 1))
		img = torch.from_numpy(img.copy()).float()
		# if self.crop_size:
		# 	_, h, w = img.size()
		# 	assert(self.crop_size < h and self.crop_size < w)
		# 	i = random.randint(0, h - self.crop_size)
		# 	j = random.randint(0, w - self.crop_size)
		# 	img = img[:, i:i+self.crop_size, j:j+self.crop_size]
		# gt = gt[:, i:i+self.crop_size, j:j+self.crop_size]
		return img

def resize_keep_ratio(img, target_size):
	# print(type(img))
	old_size = img.shape[0:2]  # 原始图像大小
	# print(old_size)
	width, height = old_size[1], old_size[0]
	width_after, height_after = target_size[1], target_size[0]
	beishu_width = width_after / width
	height_judge = height * (beishu_width)  # 先用宽测试
	if height_judge > height_after:  # 在宽度上满足，但是高度超出，需要缩小到高度直到满足
		height_new = int(height_after)
		width_new = int(width * (height_after / height))
	else:
		width_new = int(width_after)  # 在宽度上满足
		height_new = int(height_judge)
	img = cv2.resize(img, (width_new, height_new))  # resize传入的需要是整数
	pad_w = target_size[1] - width_new  # 计算需要填充的像素数目（图像的宽这一维度上）
	pad_h = target_size[0] - height_new  # 计算需要填充的像素数目（图像的高这一维度上）
	top, bottom = pad_h // 2, pad_h - (pad_h // 2)
	left, right = pad_w // 2, pad_w - (pad_w // 2)
	img_new = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, None, (0, 0, 0))  # 填充0
	print(top)
	print(left)
	return (img_new,top,bottom,left,right,old_size[0],old_size[1])


