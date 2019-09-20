# ImvboxDownloader


This python script is used to download a movie from imvbox
To run the script, you would have to:

$ python main.py media/553/1280x800 persian_cat_walk


1) It downloads the film chunks in .ts format
2) Merges all small ts chunks
3) Converts video to mp4

Requirements:

You need to install ffmpeg (which is used for step 3)

To install it in a linux machine:

$ sudo apt-get update

$ sudo apt-get install ffmpeg

To install it in a mac:

brew install ffmpeg


You also need to install python packages (requests, )

