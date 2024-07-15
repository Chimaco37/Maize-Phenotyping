![logo](https://github.com/user-attachments/assets/1392e8f6-083a-4b8b-8c88-b227d3edfdba)
# Maize Phenotyping System
> DIY ultra-affordable, high-throughput, and accurate maize phenotyping systems working at single-plant resolution in field conditions


## GUI
We developed user-friendly Graphical User Interface (GUI) for users without programming expertise.


## CLI
Phenotyping system may be used directly in the Command Line Interface (CLI).
### Setup:
- Clone the repository to your local computer:
```
git clone https://github.com/Chimaco37/Maize-Phenotyping.git
```
- Install dependancies:
```
cd Maize-Phenotyping/
pip install -r requirements.txt
```
- Download the necessary models from our Figshare repository:
https://doi.org/10.6084/m9.figshare.26282731
- Run corresponding phenotyping workflow

### 🦒The 'Giraffe' System
#### Usage
Model inference:
```bash
yolo track model=/path/to/plant_architecture.pt tracker="bytetrack.yaml" source=/path/to/your/video/folder save_txt=True save=True show_labels=True show_conf=True boxes=True conf=0.6 iou=0.5 imgsz=641 agnostic_nms=False retina_masks=True device=0 name=plant_architecture
```
Output analysis:
Example command:
`python Model_output_analysis.py [-h] -l LABEL_FOLDER -d DISTANCE_FOLDER -o OUTPUT_PATH` 
```
Analyze plant architecture data
optional arguments:
  -h, --help            show this help message and exit
  -l LABEL_FOLDER, --label_folder LABEL_FOLDER
                        Path to the label folder
  -d DISTANCE_FOLDER, --distance_folder DISTANCE_FOLDER
                        Path to the distance folder
  -o OUTPUT_PATH, --output_path OUTPUT_PATH
                        Output file path
```

### 🐿The 'Squirrel' System
#### Usage
Video Preprocessing:
Example command:
`python Convert_videos_to_projections.py [-h] -v VIDEO_FOLDER -p PARAMETER_FOLDER -o OUTPUT_PATH -c CORES_NUMBER -i PYTHON_INTERPRETER`
```
Process videos into projections
options:
  -h, --help            show this help message and exit
  -v VIDEO_FOLDER, --video_folder VIDEO_FOLDER
                        Path to the original video folder
  -p PARAMETER_FOLDER, --parameter_folder PARAMETER_FOLDER
                        Path to the image undistortion parameter folder
  -o OUTPUT_PATH, --output_path OUTPUT_PATH
                        Output undistorted image path
  -c CORES_NUMBER, --cores_number CORES_NUMBER
                        Number of cores used for parallel processing
  -i PYTHON_INTERPRETER, --python_interpreter PYTHON_INTERPRETER
                        Path to your python interpreter
```
Model inference:
###### Kernel-related traits
```
yolo segment predict model=projection.pt source=/path/to/projection/image/folder/ name='projection' device=cpu conf=0.25 iou=0.4 show_labels=False save_txt=True show_conf=False boxes=False imgsz=1600 max_det=1000 retina_masks=True
```
###### Ear-related traits
```
yolo segment predict model=ear.pt source=/path/to/ear/image/folder/ name='ear' device=cpu conf=0.5 show_labels=False show_conf=False boxes=True max_det=1 save_txt=True retina_masks=True
```
Output analysis:
Example command:
`python Model_output_analysis.py [-h] -i PROJECTION_IMAGE_FOLDER -e EAR_LABEL_FOLDER -p PROJECTION_LABEL_FOLDER -o OUTPUT_PATH -m MODEL_PATH` 
```
Analyze ear data
optional arguments:
  -h, --help            show this help message and exit
  -i PROJECTION_IMAGE_FOLDER, --projection_image_folder PROJECTION_IMAGE_FOLDER
                        Path to the projection image folder
  -e EAR_LABEL_FOLDER, --ear_label_folder EAR_LABEL_FOLDER
                        Path to the ear label folder
  -p PROJECTION_LABEL_FOLDER, --projection_label_folder PROJECTION_LABEL_FOLDER
                        Path to the projection label folder
  -o OUTPUT_PATH, --output_path OUTPUT_PATH
                        Output file path
  -m MODEL_PATH, --model_path MODEL_PATH
                        CNN model path
```

### 🦎The 'Lizard' System
#### Usage
###### Marker Segmentation
```
yolo task=segment mode=predict model=/path/to/marker.pt source=/path/to/your/original/image/folder conf=0.5 show_labels=True show_conf=False boxes=True max_det=4 save_txt=True device=cpu
```
###### Image Undistortion
`python Image_undistortion.py [-h] -i IMAGE_FOLDER -l LABEL_FOLDER -o OUTPUT_UNDISTORTED_IMAGE_PATH`
```
Undistort the image
optional arguments:
  -h, --help            show this help message and exit
  -i IMAGE_FOLDER, --image_folder IMAGE_FOLDER
                        Path to the original image folder
  -l LABEL_FOLDER, --label_folder LABEL_FOLDER
                        Path to the label folder
  -o OUTPUT_UNDISTORTED_IMAGE_PATH, --output_undistorted_image_path OUTPUT_UNDISTORTED_IMAGE_PATH
                        Output undistorted image path
```
###### Leaf Segmentation
```
yolo task=segment mode=predict model=/path/to/leaf.pt source=/path/to/your/undistorted/image/folder conf=0.5 show_labels=True show_conf=False boxes=True max_det=1 save_txt=True device=cpu
```
###### Leaf width calculation
`python Leaf_model_output_anaylsis.py [-h] -l LABEL_FOLDER -o OUTPUT_PATH`
```
Analyze leaf segmentation model output data
optional arguments:
  -h, --help            show this help message and exit
  -l LABEL_FOLDER, --label_folder LABEL_FOLDER
                        Path to the label folder
  -o OUTPUT_PATH, --output_path OUTPUT_PATH
                        Output file path
```
