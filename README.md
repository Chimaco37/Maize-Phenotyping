# Maize-Phenotyping
DIY ultra-affordable, high-throughput, and accurate maize phenotyping systems working at single-plant resolution in field conditions    

## Plant Architecture Phenotyping System
### Model Inference Command Line
yolo track model=/home/bingxing2/home/scx6853/plant_architecture_model/Final_PAPv3.pt tracker="bytetrack.yaml" source=/path/to/your/video/folder save_txt=True save=True show_labels=True show_conf=True boxes=True conf=0.6 iou=0.5 imgsz=641 agnostic_nms=False retina_masks=True device=0 name=plant_architecture


## Ear Phenotyping System
### Model Inference Command Line

##### Kernel-related traits
yolo segment predict model=projection.pt source=/path/to/projection/image/folder/ name='projection' device=cpu conf=0.25 iou=0.4 show_labels=False save_txt=True show_conf=False boxes=False imgsz=1600 max_det=1000 retina_masks=True

##### Ear-related traits
yolo segment predict model=WEP.pt source=/path/to/ear/image/folder/ name='ear' device=cpu conf=0.5 show_labels=False show_conf=False boxes=True max_det=1 save_txt=True retina_masks=True

## Leaf Phenotyping System
### Model Inference Command Line

##### Marker Segmentation
yolo task=segment mode=predict model=Marker.pt source=/path/to/your/original/image/folder conf=0.5 show_labels=True show_conf=False boxes=True max_det=4 save_txt=True device=cpu

##### Leaf Segmentation
yolo task=segment mode=predict model=Leaf.pt source=/path/to/your/undistorted/image/folder conf=0.5 show_labels=True show_conf=False boxes=True max_det=1 save_txt=True device=cpu
