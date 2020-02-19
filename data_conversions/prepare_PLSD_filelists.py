###############################################################
#																															#
#		prepare_PLSD_filelists.py																	#
#			split the file into training and testing								#
#			output: train_files_for_val_on_city_%s.txt							#
#							train_files_for_val_on_city_%s.txt							#
#																															#
#		Author: Yuheng Lu																					#
#		Mail:		yuhenglu@pku.edu.cn																#
#																															#
###############################################################

import os
import math
import random
import argparse
from datetime import datetime

DEFAULT_DATA_DIR = '../../data/PLSD'

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--folder', '-f', help='Path to data folder',default=DEFAULT_DATA_DIR)
	parser.add_argument('--h5_num', '-d', help='Number of h5 files to be loaded each time', type=int, default=8)
	parser.add_argument('--repeat_num', '-r', help='Number of repeatly using each loaded h5 list', type=int, default=2)
	args = parser.parse_args()
	print(args)
	
	root = args.folder
	
	path_dir_citys = sorted(os.listdir(root))
	city_num = len(path_dir_citys)
	city_h5s = [[] for _ in range(city_num)]
	print(city_h5s)

	for city_idx,city in enumerate(path_dir_citys):
		folder = os.path.join(root, city)
		datasets = [dataset for dataset in os.listdir(folder)]
		print(datasets)
		for dataset in datasets:
			folder_dataset = os.path.join(folder, dataset)
			filename_h5s = []
			h5_filename = os.listdir(folder_dataset)
			for filename in h5_filename:
				if filename.endswith('.h5'):
					filename_h5s.append(os.path.join(folder_dataset,filename))
					
			city_h5s[city_idx].extend(filename_h5s)
		
		print(city_h5s[city_idx])
	
	
	for city_idx,city in enumerate(path_dir_citys):
		train_h5 = []
		for idx in range(city_num):
			if idx != city_idx:
				for filename in city_h5s[idx]:
					train_h5.append(filename)
		
		random.shuffle(train_h5)
		train_list = os.path.join(root, 'train_files_for_val_on_%s.txt' % (city))
		print('{}-Saving {}...'.format(datetime.now(), train_list))
		with open(train_list, 'w') as filelist:
			list_num = math.ceil(len(train_h5) / args.h5_num)
			for list_idx in range(list_num):
				train_val_list_i = os.path.join(root, 'filelists','train_files_for_val_on_%s_g_%d.txt' % (city, list_idx))
				os.makedirs(os.path.dirname(train_val_list_i), exist_ok=True)
				with open(train_val_list_i, 'w') as filelist_i:
					for h5_idx in range(args.h5_num):
						filename_idx = list_idx * args.h5_num + h5_idx
						if filename_idx > len(train_h5) - 1:
							break
						filename_h5 = train_h5[filename_idx]
						filelist_i.write('../' + filename_h5 + '\n')
				for repeat_idx in range(args.repeat_num):
					filelist.write('./filelists/train_files_for_val_on_%s_g_%d.txt\n' % (city, list_idx))
		
		val_h5 = city_h5s[city_idx]
		val_list = os.path.join(root, 'val_files_%s.txt' % city)
		print('{}-Saving {}...'.format(datetime.now(), val_list))
		with open(val_list, 'w') as filelist:
			for filename_h5 in val_h5:
				filelist.write(filename_h5+'\n')

	
	
if __name__ == '__main__':
	main()