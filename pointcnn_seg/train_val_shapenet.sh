#!/usr/bin/env bash

gpu=
setting=
models_folder="../../models/seg/"
train_files="../../data/shapenet_partseg/train_val_files.txt"
val_files="../../data/shapenet_partseg/test_files.txt"

usage() { echo "train/val pointcnn_seg with -g gpu_id -x setting options"; }

gpu_flag=0
setting_flag=0
while getopts g:x:h opt; do
  case $opt in
  g)
    gpu_flag=1;
    gpu=$(($OPTARG))
    ;;
  x)
    setting_flag=1;
    setting=${OPTARG}
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

if [ ! -d "$models_folder" ]
then
  mkdir -p "$models_folder"
fi


echo "I am here"
echo $train_files
echo $val_files
echo $models_folder
echo $setting
echo $models_folder




python ../train_val_seg.py -t $train_files -v $val_files -s $models_folder -m pointcnn_seg -x $setting > $models_folder/pointcnn_seg_$setting.txt 2>&1 &

echo "Train/Val with setting $setting on GPU $gpu!"
CUDA_VISIBLE_DEVICES=$gpu 

python train_val_seg.py -t ../data/shapenet_partseg/train_val_files.txt -v ../data/shapenet_partseg/test_files.txt -s ../models/seg/ -m pointcnn_seg -x shapenet_x8_2048_fps