# Video Compression using Gaussian Process Regression
This does Gaussian Process Regression by taking a 10 second video (30fps), having 300 frames.
Then taking x=10 frames out of it at periodic intervals, to generate a compressed video (30:1 compression). Then to take these x frames and generate all the 300 frames out of it using pixel wise Gaussian Process Regression.

## Run Instructions - This required MATLAB
1. Keep the original video in the video directory, and name it 'video.mp4'
2. Then call this MATLAB command to reduce the video into frames, which gets stored in frames_original directory (TO BE RUN IN MATLAB terminal)
```
>> video2frames   
```
3. Then compress and decompress the video. You can change number of frames from 10 to whatever you want in the script compress_video.py
```
python compress_video.py
```
4. The above code runs for some good chunk of time, and stores the reconstructed frames in frames_reconstructed.py

5. Finally combine the frames to create the compressed video (TO BE RUN IN MATLAB)
```
>> frames2video
```
6. The regenerated video obtained by doing GBP on just x(=10) frames is stored in video_recovered directory

## RESULT
Original Video

[![Original Video](http://i3.ytimg.com/vi/G_I42XwoxBg/hqdefault.jpg)](https://www.youtube.com/watch?v=G_I42XwoxBg)

<<<<<<< HEAD
Fully Regenerated Video by taking just 10 periodic frames from the Original Video (300 frames)
=======
Fully Regenerated Video by taking just 10 periodic frames from the Original Video

>>>>>>> 7012a2430c5172c25e42f1a9212627a3cbd96c5a
[![30 by 1 Compression - Regeneration Video](http://i3.ytimg.com/vi/EZ-6bKy1Yks/hqdefault.jpg)](https://www.youtube.com/watch?v=EZ-6bKy1Yks)

Fully Regenerated Video by taking just 40 periodic frames from the Original Video (300 frames)
[![30 by 4 Compression - Regeneration Video](http://i3.ytimg.com/vi/UyQRQxTs0l4/hqdefault.jpg)](https://www.youtube.com/watch?v=UyQRQxTs0l4&feature=youtu.be)
## NOTE:
1. This is super-slow. To compress and regenerate a 7 second HD video, it took 3 hours. This can be expected as Gaussian Processes are O(n^3).
2. However it is a non-parametric Regression process, and thus we don't need to come up with models for our parameters. No headaches of it being linear, non-linear etc. On the positive, the GP model, is more close to data.
3. This is no way a useful thing, due to the slowness of Gaussian Processes. However it can be improved as each of the 720 x 1280 GP processes can be executed in parallel. I am trying to setup multiprocessing for this. If that is successful. The compute time can reduce 2-3 times. Still not much (as it will still take 30 minutes to compress and decompress). But there is embarrassingly parallel nature of this work, so there is scope of linear improvement given more process nodes that can run concurrently.
