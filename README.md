## Generate depth map from mono image in one request

REST API based on [monodepth project](https://github.com/mrharicot/monodepth)

<!-- TOC depthFrom:1 depthTo:3 withLinks:1 updateOnSave:1 orderedList:0 -->

* [Preamble](#preamble)
* [Setup](#setup)
  - [Docker](#docker)
  - [Virtualenv](#virtualenv)
  - [Configs](#configs)
* [API overview](#api-overview)
  - [Endpoints](#endpoints)
    - [Available CNNs](#available-cnns)
    - [Abailable models](#available-models)
    - [Depth map](#depth-map)
  - [Examples](#examples)
    - [cURL](#curl)
    - [Python](#python)

<!-- /TOC -->
## Preamble

## Setup

### Docker
### Virtualenv
### Configs

## API overview  

### Endpoints  

#### Available CNNs  

#### Available models

#### Depth map

### Examples  

#### cURL
```
curl -F 'image=@test.jpg' http://localhost:5000/v1/cnns/monodepth/kitti -o result.png
```
#### Python
``` 
import requests

url = 'http://localhost:5000/v1/cnns/monodepth/kitti'
files = {'image': open('test.jpg', 'rb')}

r = requests.post(url, files=files)
if r.status_code == 200:
    with open("result.png", 'wb') as f:
        f.write(r.content)
        f.close()      
```
