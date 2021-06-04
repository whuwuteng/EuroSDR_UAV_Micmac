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

### Ground control points

### Bundle adjustment compensation

## TODO



## Acknowledge

If you think you have any problem, contact [Teng Wu]<whuwuteng@gmail.com>

