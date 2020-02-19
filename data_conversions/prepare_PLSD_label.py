###############################################################
#																															#
#		prepare_PLSD_label.py																			#
#			load Powerline_segmentation_dataset as input(C,X,Y,Z)		#
#			output xyz.npy, label.npy																#
#																															#
#		Author: Yuheng Lu																					#
#		Mail:		yuhenglu@pku.edu.cn																#
#																															#
###############################################################


import numpy as np
import argparse
import os

'''
object_dict = {
            'ground':   		0,
            'powertower':   1,
            'powerline':    2,
            'insulator':    3}
'''

DEFAULT_DATA_DIR = '/data/lyh/lab/data/Powerline_Seg_dataset'
DEFAULT_OUTPUT_DIR = '/data/lyh/lab/data/PLSD'

p = argparse.ArgumentParser()
p.add_argument(
    "-d", "--data", dest='data_dir',
    default=DEFAULT_DATA_DIR,
    help="Path to S3DIS data (default is %s)" % DEFAULT_DATA_DIR)
p.add_argument(
    "-f", "--folder", dest='output_dir',
    default=DEFAULT_OUTPUT_DIR,
    help="Folder to write labels (default is %s)" % DEFAULT_OUTPUT_DIR)

args = p.parse_args()

def main():
	path_dir_citys = sorted(os.listdir(args.data_dir))
	for city in path_dir_citys:
		city_path = os.path.join(args.data_dir,city)
		path_dir_towers = sorted(os.listdir(city_path))
		for tower in path_dir_towers:
			path_final_output = os.path.join(args.output_dir, city, tower[0:-4])
			if not os.path.exists(path_final_output):
				os.makedirs(path_final_output)
			
			tower_path = os.path.join(city_path,tower)
			cxyz = np.loadtxt(tower_path)
			sortt = np.argsort(cxyz[:,0])
			cxyz = cxyz[sortt,...]
			cls,xyz = np.split(cxyz,[1],axis=1)
			cls = cls - 1
			print(cls.shape)
			print(xyz.shape)
			#np.savetxt("cls.txt", cls,fmt = "%d", delimiter = " ")
			#np.savetxt("xyz.txt", xyz,fmt = "%.3f", delimiter = " ")
			np.save(path_final_output+"/xyz.npy", xyz)
			np.save(path_final_output+"/label.npy", cls)
				
				

if __name__ == "__main__":
	main()