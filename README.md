# EuroSDR Multi-Platform Photogrammetry Dataset

## Introduction

This dataset is a public dataset from [ISPRS website](https://www2.isprs.org/commissions/comm1/icwg-1-2/benchmark_main/), there is a [conference paper](https://www.isprs-ann-photogramm-remote-sens-spatial-inf-sci.net/II-3-W4/135/2015/isprsannals-II-3-W4-135-2015.pdf)introduce this dataset.  All data and information can be found in the download [document](description_and_download_links_v3.pdf). Write this document is to indicate how to use [Micmac](https://github.com/micmacIGN/micmac) to process the  aerial dataset.

## Micmac pipeline

### Prepare for process

Because the images do not contain the camera information, so the camera should be defined before processing, the name is [MicMac-LocalChantierDescripteur.xml](MicMac-LocalChantierDescripteur.xml).

### Match Tie points

You an match all the image, i.e NxN, N is the image number.

``` shell
#! /bin/bash

mm3d Tapioca ".*tif" -1
```

Otherwise, if you can know which image pair you match, you can also define the match pairs to save the time. Thanks for the GPS/IMU, the initial camera position can be obtained. A [xml file](MesCouples.xml) is should to define the pairs. The the match command line is:

``` shell
#! /bin/bash

mm3d Tapioca File MesCouples.xml -1
```
### Initial Orientation

Because the [camera calibration](2014-PENTA-01.pdf) is given, in the image orientation, the intrinsic parameters do not need to be calculated. Before calculating the initial orientation, the [camera intrinsic file](AutoCal_Foc-50000_Cam-Canon_EOS_5D_Mark_II.xml) should be given. The the initial orientation can be calculated.
``` shell
#! /bin/bash

#put the intrinsic file into Ori-Calib directory
mm3d Tapas "Figee" ".*tif" InCal=Ori-Calib
```
### Ground control points

This dataset provide the ground control points(GCP) and the 2D measurements of the GCPs. But the files are in [Pix4D](https://support.pix4d.com/hc/en-us/articles/202558699-Using-GCPs) format. These files should be converted into Micmac format.

Convert the GCP file to Micmac format :
``` shell
#! /bin/bash

python3 create_gcp.py --gcp 3D_objectspace.csv --xml gcp_tp-3D.xml
```

Convert the 2D measurements to Micmac format :
``` shell
#! /bin/bash

python3 gcp_Pix4D_to_micmac.py --txt imagepoints.csv --xml gcp_tp-3D-S2D.xml --ext '.tif'
```

### Bundle adjustment compensation

After obtaining the GCP points, the initial orientation can be obtained :
``` shell
#! /bin/bash

GCPBascule ".*tif" "Ori-Figee" RTL-Bascule gcp_tp-3D.xml gcp_tp-3D-S2D.xml
```

The similarity transformation is not good enough for the final result, a bundle adjustment step is  needed.
``` shell
#! /bin/bash

Campari ".*tif" Ori-RTL-Bascule Compense-Figee GCP=[gcp_tp-3D-S3D.xml,0.05,gcp_tp-3D-S2D.xml,0.5] 
```
Then the final result is obtain, the rotation matrix is same with the computer vision.

### GCP check



## TODO

- [ ] Five cameras process
- [ ] LiDAR process

## Acknowledge

If you think you have any problem, contact [Teng Wu]<whuwuteng@gmail.com>

