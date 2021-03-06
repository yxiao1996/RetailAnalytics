WRITE = false;
trackFileName = "YOLO2DSNMSTracks.json";
maskFileName = "table_mask.mat";
imageFolder = "D:\\code_collection\\RetailAnalytics\\data\\imgs\\cam4-2\\";
[tracks, trackNames] = readTracksFromJSON(trackFileName);

maskFile = load(maskFileName);
mask = mask_2; % maskFile.table_mask;
jpgFiles = dir(strcat(imageFolder, '*.jpg'));
numFrames = numel(jpgFiles);
detectionInFrames = cell(numFrames, 1);

figure(1);
findTrackLength = @(track)(numel(track));
trackLengths = cellfun(findTrackLength, tracks);
subplot(1, 2, 1); histogram(trackLengths);
%tracks = NaiveTrackMerging(tracks, 0.01, 0.01);
trackLengths = cellfun(findTrackLength, tracks);
subplot(1, 2, 2); histogram(trackLengths);

for i = 1 : numel(tracks)
    track = tracks{i};
    for j = 1 : numel(track)
        detection = {track{j}{1}, i};
        numDetections = numel(detectionInFrames{track{j}{2}});
        detectionInFrames{track{j}{2}}{numDetections+1} = detection;
    end
end

if(WRITE)
    videoWriter = VideoWriter('tableTracks');
    open(videoWriter);
else
    figure(2);
end

for i = 1 : numFrames
    frame = imread(strcat(imageFolder, jpgFiles(i).name));
    detections = detectionInFrames{i};
    if(numel(detections) > 0)        
        markPositions = cell2mat(cellfun(@(d)(d{1}), detections, 'UniformOutput', false));
        detectNames = cellfun(@(d)(trackNames{d{2}}(2:end)), detections, 'UniformOutput', false);
        frame = insertMarker(frame, markPositions', 'Size', 6);
        frame = insertText(frame, markPositions', detectNames);
    end  
    if(WRITE)
        writeVideo(videoWriter, frame);  
    else
        h = imshow(frame);
        alphamask(mask, [0 1 0], 0.8);
        pause(0.01);
        input();
    end
    if(mod(i, 200) == 0)
        fprintf("#%d frame\n", i);
    end
end
close(videoWriter);
