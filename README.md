# c2ctube

Execute commands in a system remotely by uploading videos to Youtube.

## Usage

### Configuration

Update the *config.py* file:

```
channel_id = ""
api_key =  ""
```

- Get your Youtube Channel Id from [https://www.youtube.com/account_advanced](https://www.youtube.com/account_advanced).

- To get the API key create an application ([https://console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials)) and generate an API key ([https://console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials)).


### Create a video

The videos can be created using *generate_video.py*: enter the commands and generate the video writing "exit". The video generated is called by default *output.avi* (can be updated in *config.py*): 

```
python3 generate_video.py
```

![img1](images/image1.png)


### Run the listener and upload the video to Youtube

```
python3 main.py
```

The listener will check the Youtube channel every 300 seconds by default (can be updated in *config.py*). After finding there is a new video in the channel, the video is downloaded and the commands are executed:

![img2](images/image2.png)

![img3](images/image3.png)


## Create a binary


Compile the binary + clean files:

```
pyinstaller --onefile main.py
cp dist/main c2ctube
rm -rf dist build
rm main.spec
```

