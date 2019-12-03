trackFileName = "YOLO2DSSqrNMSTracks.json";
imageFolder = "D:\\code_collection\\RetailAnalytics\\data\\imgs\\cam2-2_square\\";
[tracks, trackNames] = readTracksFromJSON(trackFileName);

jpgFiles = dir(strcat(imageFolder, '*.jpg'));
numFrames = numel(jpgFiles);
detectionInFrames = cell(numFrames, 1);

figure(1);
findTrackLength = @(track)(numel(track));
trackLengths = cellfun(findTrackLength, tracks);
subplot(1, 2, 1); histogram(trackLengths);
%tracks = NaiveTrackMerging(tracks, 0.0005, 1);
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

videoWriter = VideoWriter('tracks');
open(videoWriter);
for i = 1 : numFrames
    frame = imread(strcat(imageFolder, jpgFiles(i).name));
    detections = detectionInFrames{i};
    if(numel(detections) > 0)        
        markPositions = cell2mat(cellfun(@(d)(d{1}), detections, 'UniformOutput', false));
        detectNames = cellfun(@(d)(trackNames{d{2}}(2:end)), detections, 'UniformOutput', false);
        frame = insertMarker(frame, markPositions', 'Size', 6);
        frame = insertText(frame, markPositions', detectNames);
    end
    %figure(2);
    %imshow(frame);
    %pause(0.01);
    writeVideo(videoWriter, frame);    
    if(mod(i, 200) == 0)
        fprintf("#%d frame\n", i);
    end
end
close(videoWriter);
