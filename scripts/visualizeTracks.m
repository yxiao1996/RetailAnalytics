trackFileName = "YOLODSCam42Trakcs.json";
videoFileName = "cam4-2.mkv";
[tracks, trackNames] = readTracksFromJSON(trackFileName);

videoReader = VideoReader(videoFileName);
numFrames = int64(videoReader.Duration * videoReader.FrameRate);
detectionInFrames = cell(numFrames, 1);

figure(1);
findTrackLength = @(track)(numel(track));
trackLengths = cellfun(findTrackLength, tracks);
subplot(1, 2, 1); histogram(trackLengths);
tracks = NaiveTrackMerging(tracks, 0.00001, 1);
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

figure(2);
videoWriter = VideoWriter('tracks');
open(videoWriter);
for i = 1 : numFrames
    frame = readFrame(videoReader);
    detections = detectionInFrames{i};
    if(numel(detections) > 0)        
        markPositions = cell2mat(cellfun(@(d)(d{1}), detections, 'UniformOutput', false));
        detectNames = cellfun(@(d)(trackNames{d{2}}(2:end)), detections, 'UniformOutput', false);
        frame = insertMarker(frame, markPositions', 'Size', 6);
        frame = insertText(frame, markPositions', detectNames);
    end
    %imshow(frame);
    writeVideo(videoWriter, frame);
    pause(0.01);
    if(mod(i, 200) == 0)
        fprintf("#%d frame\n", i);
    end
end
close(videoWriter);