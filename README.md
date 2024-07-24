![logo](https://github.com/user-attachments/assets/1392e8f6-083a-4b8b-8c88-b227d3edfdba)
# Maize Phenotyping System
> DIY ultra-affordable, high-throughput, and accurate maize phenotyping systems working at single-plant resolution in field conditions

## Features
- **Graphical User Interface (GUI):** User-friendly interface for users without programming expertise.
- **Command Line Interface (CLI):** Direct use via command line.

## Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Chimaco37/Maize-Phenotyping.git
    ```
2. **Install dependencies (Only when you need to use CLI):**

    ```bash
    cd Maize-Phenotyping/
    pip install -r requirements.txt
    ```

3. **Download necessary models:**  

    First, download the required model files from the [Models Figshare Repository](https://doi.org/10.6084/m9.figshare.26282731).
    
    **Placement of model files:**
    
    - **For the GUI of the ear phenotyping system:**
    
      Place the downloaded model files in the specified directory with the following steps:

        ```bash
        cd ear/GUI/
        unzip Models.zip
        cp Models/Ear_Models/* models/
        ```
    
    - **For Command Line Interface (CLI) usage:**
   
      You can place the models in any location that is convenient for you.

4. **Download GUIs:**

    Download the GUI files from the [GUIs Figshare Repository](https://doi.org/10.6084/m9.figshare.26363107).

    - **Placement of GUI files:**
   
      After downloading, place the GUI files in the respective ./GUI directory with these steps:
  
        ```
        cd leaf/GUI/
        unzip GUIs.zip
        cp GUIs/Lizard.exe ./
        ```

## GUI Usage
### 🦒The 'Giraffe' System
![image](https://github.com/user-attachments/assets/6d37a213-d0c5-4445-9cfa-335f4e5c00e6)

- **Model Inference:**
Press the "Model Inference" button and then the select the original video folder and results output folder, then the model would process the videos finally outputs the phenotypic data.

### 🐿️The 'Squirrel' System
![image](https://github.com/user-attachments/assets/efc8459c-55f9-4a39-a1b8-0e457a93f021)


- **Video Process:**
Press the "Video Process" button and then the select the video folder and image output folder, then the videos would be processed into projection and ear images.

- **Model inference:**
Press the "Model Inference" button and then the select the image folder and results output folder, then projection and ear images would undergo respective model inference and the model outputs would be analyzed finally output results.


### 🦎The 'Lizard' System
![image](https://github.com/user-attachments/assets/6e06a325-d988-446e-b2c6-13a2b721f2d9)

- **Model inference:**
Press the "Model Inference" button and then the select the original leaf image folder and results output folder, then the marker inference model will preocess the image, then the image would be undistorted and undergoes leaf model inference, finally output leaf width data.


## CLI Usage

### 🦒The 'Giraffe' System

- **Model training:**

```bash
yolo segment train data=/path/to/your/plant_architecture/dataset/data.yaml model=/path/to/your/plant_architecture/model.pt epochs=200 patience=30 batch=64 imgsz=640 device=0 name=plant_architecture_training
```

- **Model inference:**

```bash
yolo track model=/path/to/plant_architecture.pt tracker=/path/to/bytetrack.yaml source=/path/to/your/video/folder save_txt=True save=True show_labels=True show_conf=True boxes=True conf=0.6 iou=0.5 imgsz=641 agnostic_nms=False retina_masks=True device=0 name=plant_architecture
```
- **Output analysis:**
```
python Model_output_analysis.py -l LABEL_FOLDER -d DISTANCE_FOLDER -o OUTPUT_PATH

optional arguments:
  -l: Path to the model output label folder (default is ./labels/)
  -d: Path to the corresponding distance folder of the videos (default is ./distances/)
  -o: Analyzed results output folder (default is ./)
```

### 🐿️The 'Squirrel' System

- **Video Preprocessing:**
```
python Convert_videos_to_projections.py -v VIDEO_FOLDER -p PARAMETER_FOLDER -o OUTPUT_PATH -c CORES_NUMBER -i PYTHON_INTERPRETER

optional arguments:
  -v: Path to the original video folder (default is ./videos/)
  -p: Path to the image undistortion parameter folder (default is ./image_process/)
  -o: Output undistorted image folder (default is ./undistorted/)
  -c: Number of cores used for parallel processing (default is 5)
  -i: Path to your python interpreter
```

- **Model training for kernel-related and ear-related traits:**

```bash
yolo segment train data=/path/to/your/projection/dataset/data.yaml model=/path/to/your/projection/model.pt epochs=200 batch=4 patience=30 device=0,1,2,3 name=projection_model_training
yolo segment train data=/path/to/your/ear/dataset/data.yaml model=/path/to/your/ear/model.pt epochs=200 batch=32 patience=30 device=0 name=ear_model_training
```

- **Model inference for kernel-related and ear-related traits:**

```
yolo segment predict model=projection.pt source=/path/to/projection/image/folder/ device=cpu conf=0.25 iou=0.4 show_labels=False save_txt=True show_conf=False boxes=False imgsz=1600 max_det=1000 retina_masks=True  name=projection

yolo segment predict model=ear.pt source=/path/to/ear/image/folder/ device=cpu conf=0.5 show_labels=False show_conf=False boxes=True max_det=1 save_txt=True retina_masks=True name=ear
```
- **Output analysis:**
```
python Model_output_analysis.py -i PROJECTION_IMAGE_FOLDER -e EAR_LABEL_FOLDER -p PROJECTION_LABEL_FOLDER -o OUTPUT_PATH -m MODEL_PATH

optional arguments:
  -i: Path to the projection image folder (default is ./images/projection/)
  -e: Path to the ear model output label folder (default is ./result/ear/labels/)
  -p: Path to the projection model output label folder (default is ./result/projection/labels/)
  -o: Analyzed results output folder (default is ./)
  -m: CNN model path folder (default is ./models/)
```


### 🦎The 'Lizard' System
- **Model training for marker and leaf:**

```bash
yolo segment train data=/path/to/your/marker/dataset/data.yaml model=model=/path/to/your/marker/model.pt epochs=200 batch=32 device=0 name=marker_model_training
yolo segment train data=/path/to/your/leaf/dataset/data.yaml model=model=/path/to/your/leaf/model.pt epochs=200 batch=32 device=0 name=leaf_model_training
```

- **Marker Segmentation:**

```
yolo task=segment mode=predict model=/path/to/marker.pt source=/path/to/your/original/image/folder conf=0.5 show_labels=True show_conf=False boxes=True max_det=4 save_txt=True device=cpu name=marker
```
- **Image Undistortion:**
```
python Image_undistortion.py -i IMAGE_FOLDER -l LABEL_FOLDER -o OUTPUT_UNDISTORTED_IMAGE_PATH

optional arguments:
  -i: Path to the original image folder (default is ./images/)
  -l: Path to the marker model output label folder (default is ./marker/labels/)
  -o: Output undistorted image folder (default is ./undistorted/)
```
- **Marker Segmentation:**
```
yolo task=segment mode=predict model=/path/to/leaf.pt source=/path/to/your/undistorted/image/folder conf=0.5 show_labels=True show_conf=False boxes=True max_det=1 save_txt=True device=cpu name=leaf
```
- **Leaf width calculation:**
```
python Leaf_model_output_anaylsis.py -l LABEL_FOLDER -o OUTPUT_PATH

optional arguments:
  -l: Path to the leaf model output label folder (default is ./leaf/labels/)
  -o: Analyzed results output folder (default is ./)
```
