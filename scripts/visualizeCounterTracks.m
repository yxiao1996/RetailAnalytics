WRITE = false;
EASY = false;
trackFileName = "YOLO2DSSqrNMSTracks.json";
maskFileName = "counter_mask_large.mat";
imageFolder = "D:\\code_collection\\RetailAnalytics\\data\\imgs\\cam2-2_square\\";

if(EASY)
    startFrame = 900;
    endFrame = 1099;
else
    startFrame = 200;
    endFrame = 399;
end

[tracks, trackNames] = readTracksFromJSON(trackFileName);

maskFile = load(maskFileName);
counterMask = maskFile.mask_2;
jpgFiles = dir(strcat(imageFolder, '*.jpg'));
numFrames = numel(jpgFiles);
detectionInFrames = cell(numFrames, 1);

for i = 1 : numel(tracks)
    track = tracks{i};
    for j = 1 : numel(track)
        detection = {track{j}{1}, i};
        numDetections = numel(detectionInFrames{track{j}{2}});
        detectionInFrames{track{j}{2}}{numDetections+1} = detection;
    end
end

if(WRITE)
    videoWriter = VideoWriter('counterTracks');
    videoWriter.FrameRate = 20;
    open(videoWriter);
else
    figure(2);
end

for i = startFrame : endFrame
    frame = imread(strcat(imageFolder, jpgFiles(i).name));
    detections = detectionInFrames{i};
    if(numel(detections) > 0)        
        markPositions = cell2mat(cellfun(@(d)(d{1}), detections, 'UniformOutput', false));
        detectNames = cellfun(@(d)(trackNames{d{2}}(2:end)), detections, 'UniformOutput', false);
        frame = insertMarker(frame, markPositions', 'Size', 6);
        frame = insertText(frame, markPositions', detectNames);
    end  
    
    h = imshow(frame);
    alphamask(counterMask, [0 1 0], 0.8);
    
    if(WRITE)
        outputFrame = getframe(gcf);
        writeVideo(videoWriter, outputFrame); 
    else
        pause(0.01);
        input();
    end
    if(mod(i, 200) == 0)
        fprintf("#%d frame\n", i);
    end
end
close(videoWriter);
