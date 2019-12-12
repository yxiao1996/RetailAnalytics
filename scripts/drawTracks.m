EASY = false;

trackFileName = "YOLO2DSSqrNMSTracks.json";
imageFolder = "D:\\code_collection\\RetailAnalytics\\data\\imgs\\cam2-2_square\\";

if(EASY)
    startTime = 980;
    endTime = 1010;
else
    startTime = 780;
    endTime = 820;
end

[tracks, trackNames] = readTracksFromJSON(trackFileName);
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

colors = {'green','white','red','magenta', 'yellow', 'blue', 'black', ...
          'green','white','red','magenta', 'yellow', 'blue', 'black', ...
          'green','white','red','magenta', 'yellow', 'blue', 'black'};

initialTrackNames = cellfun(@(d)num2str(d{2}), detectionInFrames{startTime}, 'UniformOutput', false);
initialTrackLocs = cellfun(@(d)(d{1}'), detectionInFrames{startTime}, 'UniformOutput', false);
initialTrackLocs = cat(1, initialTrackLocs{:});
finalTrackNames = cellfun(@(d)num2str(d{2}), detectionInFrames{endTime}, 'UniformOutput', false);
finalTrackLocs = cellfun(@(d)(d{1}'), detectionInFrames{endTime}, 'UniformOutput', false);
finalTrackLocs = cat(1, finalTrackLocs{:});

trackDrawNames = {};
trackDraw = {};
for i = startTime : endTime
    detections = detectionInFrames{i};
    for j = 1 : numel(detections)
        d = detections{j};
        if(ismember(num2str(d{2}), trackDrawNames))
            [~, idx] = ismember(num2str(d{2}), trackDrawNames);
            trackDraw{idx}{numel(trackDraw{idx})+1} = d{1};
        else
            trackDrawNames{numel(trackDrawNames)+1} = num2str(d{2});
            trackDraw{numel(trackDraw)+1} = {d{1}};
        end
    end
end


startFrame = imread(strcat(imageFolder, jpgFiles(startTime).name));
[~, initNameIdx] = ismember(initialTrackNames, trackDrawNames);
startFrame = insertMarker(startFrame, initialTrackLocs, 'square', 'color', colors(initNameIdx), 'size', 5);
startFrame = insertText(startFrame, initialTrackLocs, initialTrackNames);
endFrame = imread(strcat(imageFolder, jpgFiles(endTime).name));
endFrame = insertText(endFrame, finalTrackLocs, finalTrackNames);
for i = 1 : numel(trackDraw)
    t = trackDraw{i};
    trackLocs = cat(2, t{:})';
    endFrame = insertMarker(endFrame, trackLocs, 'square', 'color', colors{i}, 'size', 5);
    if(numel(trackLocs) > 2)
        lineLocs = zeros(2*size(trackLocs, 1), 1);
        for j = 1 : size(trackLocs, 1)
            lineLocs(2*j-1 : 2*j) = trackLocs(j, :);
        end
        endFrame = insertShape(endFrame, 'Line', lineLocs', 'color', colors{i}, 'LineWidth', 3);
    end
end

figure(1);
imshow(startFrame);
figure(2);
imshow(endFrame);