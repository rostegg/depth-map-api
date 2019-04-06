## Generate depth map from mono image in one request with CNNs (Convolutional neural networks)
### REST API based on [monodepth project](https://github.com/mrharicot/monodepth) (and other in future)

![](../assets/example.jpeg) ![](../assets/example_depth.png) 
<!-- TOC depthFrom:1 depthTo:3 withLinks:1 updateOnSave:1 orderedList:0 -->
* [Setup](#setup)
  - [Docker](#docker)
  - [Virtualenv](#virtualenv)
  - [Configs](#configs)
  - [Cache](#cache)
  - [CNNs setup](#cnns-setup)
    - [Monodepth](#monodepth)
* [API overview](#api-overview)
  - [Endpoints](#endpoints)
    - [Available CNNs](#available-cnns)
    - [Abailable models](#available-models)
    - [Depth map](#depth-map)
  - [Examples](#examples)
    - [cURL](#curl)
    - [Python](#python)
<!-- /TOC -->

## Setup
This section describes possible ways to deploy an application and app and deploy environment setup.
There are two main ways to deploy an application: 
* Using `docker-compose`, which create isolated environment without dependency conflict (and also redis instance for caching)
* Or just run `run.py` script, but then you have to deploy the redis instance yourself (more in [cache](#cache) section)
  
### Docker
For build image use `docker-compose build`, it deploy project and automatically downloads all necessary dependencies and models for CNNs.  
After build execute with `docker-compose up` or better use `run-docker.sh` script, which propose docker compose run mode (press `Enter` for execute in default mode, or type something and press `Enter` to run in demon mode)  
Then you can access app on localhost:5000
### Virtualenv
First, run `get_models_monodepth.sh` script, which downloads required models 
Use `run-env.sh` script which setup virtual environment, install depedncies and run app.
### Configs
All environments variable ([about flask variables](http://flask.pocoo.org/docs/1.0/config/)) setted in `config.env` file and loading in `config.py`, where you can create own app config mode.
### Cache
By default app support caching using Redis. For custom redis url set `CACHE_REDIS_URL` variable in `config.env`.  
If you don't want to create redis instance or use docker, just change `CACHE_TYPE` to `simple`, and comment out 
`CACHE_REDIS_URL = os.environ.get('CACHE_REDIS_URL')` line in `config.py` (if you left `CACHE_REDIS_URL` variable in `config.env`, then it is not necessary)
### CNNs setup
At the moment, there is only one CNN. When adding others, all logic will be described in `cnn_name_bridge.py` files
#### Monodepth
`monodepth_bridge.py` initializes all necessary models in advance, to avoid a long delay.  
Model also has static input values for the height and width of the image (height - 256px and width - 512px), to maintain performance (this is especially noticeable when running on a CPU).  
If GPU is used for calculations, change `self_width` and `self_height` in `monodepth_bridge.py`, or reinit models params for image. You can use method like this, for calculate optimal width and heigh and limit the size of the input image:  
```
# image - BytesIO(image_bytes_arr)
def get_optimal_image_size(image):
    input_image = scipy.misc.imread(self.image_bytes, mode="RGB")
    # example for max 1248*960
    width, height, num_channels  = input_image.shape
    width = (1248 if(width > 1248) else (width - (width % 32)))
    height = (960 if(height > 960) else (height - (height % 32)))
    return width, height
```
## API overview  

| Resource| Method | Description |
| --------| --------|--------|
| [/](#available-cnns)|GET|Return list of available CNNs|
| [/v1/cnns](#available-cnns)|GET|Return list of available CNNs|
| [/v1/cnns/{cnn_name}](#available-models)|GET|Return list of available models for CNN|
| [/v1/cnns/{cnn_name}/{model}](#depth-map)|POST|Return predicted depth map (in `png` format) of image, using selected model|

### Endpoints 

#### Available CNNs  
Return array of available CNNs with external links to projects
* URL: [/] or [/v1/cnns]
* Method: GET
* Success Response:  
  - Code: 200  
  - Content: [{"name": "monodepth", "ext_link": "https://github.com/mrharicot/monodepth"}]
* Error Response:  
  - Code: 400
  - Content: {'message':'Bad Request error'}
------------------------
#### Available models
Return array of available models for selected CNN
* URL: [/v1/cnns/{cnn_name}]
* Method: GET
* URL params: 
  - Required: `cnn_name=string` (received from [GET /v1/cnns](#available-cnns) request in `name` filed)
* Success Response:  
  - Code: 200  
  - Content: ["kitti", "cityscapes", "eigen"]
* Error Response:  
  - Code: 400
  - Content: {'message':'Bad Request error'}
------------------------
#### Depth map
Return predicted depth map image in `png` format
* URL: [/v1/cnns/{cnn_name}/{model}]
* Method: POST
* URL params: 
  - Required:  
  `cnn_name=string` (received from [GET /v1/cnns](#available-cnns) request in `name` filed)   
  `model=string` (received from [GET /v1/cnns/{cnn_name}](#available-models) request)  
* Data params:  
  - Image data with `image` form name, example below.  
  - Supported image formats : `png`, `jpg`, `jpeg`
* Request example:  
```
POST /v1/cnns/monodepth/jitti
.....Here headings we are not interested in......
Content-Length: 2740
Content-Type: multipart/form-data;  boundary=----6PA4QswqtyuhfgxkTrZu0gW

----6PA4QswqtyuhfgxkTrZu0gW
Content-Disposition: form-data; name="image"; filename="test.jpg"
...........Here image data............
----6PA4QswqtyuhfgxkTrZu0gW
```
* Success Response:
  ```
  HTTP/1.0 200 OK
  Content-Disposition: attachment; filename=cat.png
  Content-Type: image/png
  .....Image binary data........
  ```
* Error Response:  
  - Code: 400
  - Content: {'message':'Bad Request error'}
### Examples  
In this section described examples for POST request to generate depth map from image
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
