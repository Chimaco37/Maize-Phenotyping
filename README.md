![logo](https://github.com/user-attachments/assets/1392e8f6-083a-4b8b-8c88-b227d3edfdba)
# Maize Phenotyping System
> DIY ultra-affordable, high-throughput, and accurate maize phenotyping systems working at single-plant resolution in field conditions

## Features

- **Graphical User Interface (GUI):** User-friendly interface for users without programming expertise.
- **Command Line Interface (CLI):** Direct use via command line.

## Setup

1. **Clone the repository:**
```
git clone https://github.com/Chimaco37/Maize-Phenotyping.git
```
2. **Install dependencies:**
```
cd Maize-Phenotyping/
pip install -r requirements.txt
```
3. **Download necessary models:**
- [Figshare Repository](https://doi.org/10.6084/m9.figshare.26282731)

## CLI Usage

### 🦒The 'Giraffe' System

- **Model inference:**

```bash
yolo track model=/path/to/plant_architecture.pt tracker="bytetrack.yaml" source=/path/to/your/video/folder save_txt=True save=True show_labels=True show_conf=True boxes=True conf=0.6 iou=0.5 imgsz=641 agnostic_nms=False retina_masks=True device=0 name=plant_architecture
```
- **Output analysis:**
```
python Model_output_analysis.py -l LABEL_FOLDER -d DISTANCE_FOLDER -o OUTPUT_PATH

optional arguments:
  -l LABEL_FOLDER,      Path to the model output label folder
  -d DISTANCE_FOLDER,   Path to the corresponding distance folder of the videos
  -o OUTPUT_PATH,       Analyzed results output folder
```


### 🐿️The 'Squirrel' System

- **Video Preprocessing:**
```
python Convert_videos_to_projections.py -v VIDEO_FOLDER -p PARAMETER_FOLDER -o OUTPUT_PATH -c CORES_NUMBER -i PYTHON_INTERPRETER

options:
  -v VIDEO_FOLDER,       Path to the original video folder
  -p PARAMETER_FOLDER,   Path to the image undistortion parameter folder
  -o OUTPUT_PATH,        Output undistorted image folder
  -c CORES_NUMBER,       Number of cores used for parallel processing
  -i PYTHON_INTERPRETER, Path to your python interpreter
```
- **Model inference for Kernel-related and Ear-related traits:**

```
yolo segment predict model=projection.pt source=/path/to/projection/image/folder/ name='projection' device=cpu conf=0.25 iou=0.4 show_labels=False save_txt=True show_conf=False boxes=False imgsz=1600 max_det=1000 retina_masks=True

yolo segment predict model=ear.pt source=/path/to/ear/image/folder/ name='ear' device=cpu conf=0.5 show_labels=False show_conf=False boxes=True max_det=1 save_txt=True retina_masks=True
```
- **Output analysis:**
```
python Model_output_analysis.py -i PROJECTION_IMAGE_FOLDER -e EAR_LABEL_FOLDER -p PROJECTION_LABEL_FOLDER -o OUTPUT_PATH -m MODEL_PATH

optional arguments:
  -i PROJECTION_IMAGE_FOLDER,  Path to the projection image folder
  -e EAR_LABEL_FOLDER,         Path to the ear model output label folder
  -p PROJECTION_LABEL_FOLDER,  Path to the projection model output label folder
  -o OUTPUT_PATH,              Analyzed results output folder
  -m MODEL_PATH,               CNN model path folder
```


### 🦎The 'Lizard' System

- **Marker Segmentation:**

```
yolo task=segment mode=predict model=/path/to/marker.pt source=/path/to/your/original/image/folder conf=0.5 show_labels=True show_conf=False boxes=True max_det=4 save_txt=True device=cpu
```
- **Image Undistortion:**
```
python Image_undistortion.py -i IMAGE_FOLDER -l LABEL_FOLDER -o OUTPUT_UNDISTORTED_IMAGE_PATH

optional arguments:
  -i IMAGE_FOLDER,                   Path to the original image folder
  -l LABEL_FOLDER,                   Path to the marker model output label folder
  -o OUTPUT_UNDISTORTED_IMAGE_PATH,  Output undistorted image folder
```
- **Marker Segmentation:**
```
yolo task=segment mode=predict model=/path/to/leaf.pt source=/path/to/your/undistorted/image/folder conf=0.5 show_labels=True show_conf=False boxes=True max_det=1 save_txt=True device=cpu
```
- **Leaf width calculation:**
```
python Leaf_model_output_anaylsis.py -l LABEL_FOLDER -o OUTPUT_PATH`

optional arguments:
  -l LABEL_FOLDER,  Path to the leaf model output label folder
  -o OUTPUT_PATH,   Analyzed results output folder
```
