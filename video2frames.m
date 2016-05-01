%% Script - That converts a video into a set of frames for GPR compression
% Get the video
v = VideoReader('video/video.mp4');
video = read(v,[1 inf]);

% Store each frame in the frames as a matlab in grayscale 
num_frames = size(video,4);

for frame_id = 1:num_frames
    image = video(:,:,:,frame_id);
    image_gray = rgb2gray(image);
    file_name = strcat('frames_original/frame_', int2str(frame_id), '.mat');
    save(file_name,'image_gray')
end

% store the frame rate
frame_rate = v.FrameRate();
save('frames_original/input_frame_rate.mat', 'frame_rate');

% store the number of frames
save('frames_original/input_num_frames.mat', 'num_frames');




