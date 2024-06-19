# Maize-Phenotyping
Ultra-affordable, high-throughput, accurate phenotyping of maize at single-plant resolution in field conditions


## Ear Phenotyping System
### Model Inference Command Line (Linux)

##### Kernel-related traits
yolo segment predict model=projection.pt source=/path/to/projection/image/folder/ name='projection' device=cpu conf=0.25 iou=0.4 show_labels=False save_txt=True show_conf=False boxes=False imgsz=1600 max_det=1000 retina_masks=True

##### Ear-related traits
yolo segment predict model=WEP.pt source=/path/to/ear/image/folder/ name='ear' device=cpu conf=0.5 show_labels=False show_conf=False boxes=True max_det=1 save_txt=True retina_masks=True
