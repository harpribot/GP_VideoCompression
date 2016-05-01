%% Script to convert a set of given frames into a video
outputVideo = VideoWriter('video_recovered/video_compressed.avi');
inp_vid_inf = load('frames_original/input_frame_rate.mat');
input_frame_rate = inp_vid_inf.frame_rate;

% Set output video frame
outputVideo.FrameRate = input_frame_rate;

% open output video
open(outputVideo)

% store the frame into the output video
frame_info = load('frames_original/input_num_frames.mat');
input_num_frames = frame_info.num_frames;

% Write the frame to the video
frameNames = dir(fullfile('frames_reconstructed','*.mat'));
frameNames = {frameNames.name}';

% assert that the number of frames are the same 
assert(length(frameNames) == input_num_frames, 'The output is lossy. Input frame cnt. not equal to output frame cnt.')

for frame_id = 1:length(frameNames)
   framefile = strcat('frame_', int2str(frame_id), '.mat');
   image = load(fullfile('frames_reconstructed',framefile));
   image = image.image_gray;
   image = mat2gray(image);
   writeVideo(outputVideo,image);
end
