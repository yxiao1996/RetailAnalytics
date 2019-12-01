function videoFrames = readFramesFromVideoIntoArray(fileName, toGrayscale)
    videoReader = VideoReader(fileName);
    numFrames = int64(videoReader.Duration * videoReader.FrameRate);
    if(toGrayscale)
        videoFrames = zeros(numFrames, videoReader.Height, videoReader.Width);   % grayscale
    else
        videoFrames = zeros(numFrames, videoReader.Height, videoReader.Width, 3);% color
    end
    for i = 1 : numFrames
        frame = readFrame(videoReader);
        if(toGrayscale)
            frame = rgb2gray(frame);
            videoFrames(i, :, :) = frame;
        else
            videoFrames(i, :, :, :) = double(frame) / 255;
        end
    end
end

