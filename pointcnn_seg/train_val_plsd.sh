#!/usr/bin/env bash

gpu=
setting=
area=
models_folder="../../models/seg/"
data_folder="../../data/s3dis/"

usage() { echo "train/val pointcnn_seg with -g gpu_id -x setting -a area options"; }

gpu_flag=0
setting_flag=0
area_flag=0
while getopts g:x:a:h opt; do
  case $opt in
  g)
    gpu_flag=1;
    gpu=$(($OPTARG))
    ;;
  x)
    setting_flag=1;
    setting=${OPTARG}
    ;;
  a)
    area_flag=1;
    area=$(($OPTARG))
    ;;
  h)
    usage; exit;;
  esac
done

shift $((OPTIND-1))

if [ $gpu_flag -eq 0 ]
then
  echo "-g option is not presented!"
  usage; exit;
fi

if [ $setting_flag -eq 0 ]
then
  echo "-x option is not presented!"
  usage; exit;
fi

if [ $area_flag -eq 0 ]
then
  echo "-a option is not presented!"
  usage; exit;
fi

if [ ! -d "$models_folder" ]
then
  mkdir -p "$models_folder"
fi

echo $data_folder
echo $models_folder
echo $setting


echo "Train/Val with setting $setting on GPU $gpu for Area $area!"
CUDA_VISIBLE_DEVICES=$gpu 
python train_val_seg.py -t ../data/S3DIS/prepare_label_rgb/train_files_for_val_on_Area_1.txt -v ../data/S3DIS/prepare_label_rgb/val_files_Area_1.txt -s ../models/seg/ -m pointcnn_seg -x s3dis_x8_2048_fps

python train_val_seg.py -t ../data/PLSD_tmp/train_files_for_val_on_wenzhou_seg.txt -v ../data/PLSD_tmp/val_files_wenzhou_seg.txt -s ../models/seg/ -m pointcnn_seg -x plsd_x8_2048_fps
