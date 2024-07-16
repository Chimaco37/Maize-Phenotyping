import os
import subprocess
from multiprocessing import Pool
import argparse

# Create the parser
parser = argparse.ArgumentParser(description="Process videos into projections")

# Add arguments
parser.add_argument('-v', '--video_folder', default='./videos/', type=str, required=True, help='Path to the original video folder')
parser.add_argument('-p', '--parameter_folder', default='./image_process/', type=str, required=True,
                    help='Path to the image undistortion parameter folder')
parser.add_argument('-o', '--output_path',  default='./undistorted/', type=str, required=True, help='Output undistorted image path')
parser.add_argument('-c', '--cores_number', default=5, type=int, required=True,
                    help='Number of cores used for parallel processing')
parser.add_argument('-i', '--python_interpreter', type=str, required=True,
                    help='Path to your python interpreter')


# Parse the arguments
args = parser.parse_args()

# Create necessary directories under the output path
ear_dir = os.path.join(args.output_path, 'ear/')
projection_dir = os.path.join(args.output_path, 'projection/')
os.makedirs(ear_dir, exist_ok=True)
os.makedirs(projection_dir, exist_ok=True)

def generate_script(run):
    full_run = os.path.join(target_path, run)
    script_file_name = os.path.join(target_path, 'command_' + run)

    with open(script_file_name, 'w') as script_file:
        script_file.write('#!/bin/bash\n')
        script_file.write(f'ffmpeg -i {full_run} -threads 2 {full_run}_frame%03d.png\n')

        script_file.write(f'{args.python_interpreter}  << EOF\n')
        script_file.write('from image_process.camera_functions import undistort_and_resize_image\n')
        script_file.write('import numpy as np\n')
        script_file.write('import glob\n')
        script_file.write(f'mtx = np.load("{args.parameter_folder}/HQ_camera_1072_1440_mtx_dist.npz")["x"]\n')
        script_file.write(f'dist = np.load("{args.parameter_folder}/HQ_camera_1072_1440_mtx_dist.npz")["y"]\n')
        script_file.write(f'images = glob.glob("{full_run}_frame*.png")\n')
        script_file.write('for fname in images:\n')
        script_file.write('    undistort_and_resize_image(fname, mtx, dist, 1072, 1440)\n')
        script_file.write('EOF\n')

        script_file.write(f'rm {full_run}_frame*.png\n')
        script_file.write(f'convert {full_run}_undistort*.png -crop 1x1440+536+0 +repage {full_run}_pixel%03d.png\n')
        script_file.write(f'cp {full_run}_undistort100.png {ear_dir}{run}_phenotyping_1.png\n')
        script_file.write(f'cp {full_run}_undistort116.png {ear_dir}{run}_phenotyping_2.png\n')
        script_file.write(f'cp {full_run}_undistort132.png {ear_dir}{run}_phenotyping_3.png\n')
        script_file.write(f'cp {full_run}_undistort148.png {ear_dir}{run}_phenotyping_4.png\n')
        script_file.write(f'cp {full_run}_undistort164.png {ear_dir}{run}_phenotyping_5.png\n')
        script_file.write(f'cp {full_run}_undistort180.png {ear_dir}{run}_phenotyping_6.png\n')
        script_file.write(f'rm {full_run}_undistort*.png\n')
        script_file.write(f'convert {full_run}_pixel*.png +append +repage {full_run}_raw.png\n')
        script_file.write(f'rm {full_run}_pixel*.png\n')
        script_file.write(f'convert {full_run}_raw.png -resize 480x1440! {full_run}_resize.png\n')
        script_file.write(f'rm {full_run}_raw.png\n')
        script_file.write(f'convert {full_run}_resize.png -crop 450x1440+40+0 +repage {full_run}_without_resize.png\n')
        script_file.write(f'rm {full_run}_resize.png\n')
        script_file.write(f'convert {full_run}_without_resize.png -resize 480x1440! {full_run}.png\n')
        script_file.write(f'rm {full_run}_without_resize.png\n')
        script_file.write(f'rm {script_file_name}\n')
        script_file.write(f'mv {full_run}.png {projection_dir}\n')

    return script_file_name

def process_file(file):
    run = file.split('/')[-1]
    script_file_name = generate_script(run)
    print(f"Script generated for {run}")
    subprocess.run(['bash', script_file_name])
    print(f"Script submitted for {run}")

if __name__ == '__main__':
    # 设置目标路径
    target_path = args.video_folder

    # 获取所有视频文件名
    all_files_with_extensions = [
        os.path.join(dp, f) for dp, dn, filenames in os.walk(target_path)
        for f in filenames if f.lower().endswith(('.mp4', '.avi'))
    ]

    all_files = []  # 用来存储重命名后的文件路径

    for file_path in all_files_with_extensions:
        directory, filename = os.path.split(file_path)
        filename_without_ext, ext = os.path.splitext(filename)
        new_file_path = os.path.join(directory, filename_without_ext)
        os.rename(file_path, new_file_path)
        all_files.append(filename_without_ext)

    num_cores = args.cores_number

    # 并行处理文件
    with Pool(num_cores) as pool:
        pool.map(process_file, all_files)
