COUNTER = false;
MERGE_TRACK = false;

% filenames
counterTrackFileName = "YOLO2DSSqrNMSTracks.json";
counterMaskFileName = "counter_mask_very_large.mat";
tableTrackFileName = "YOLO2DSNMSTracks.json";
tableMaskFileName = "table_mask.mat";

% parameters
minDwellTime = 50;
probTresh = 0.001;
wienerVar = 0.01;

% handles
findTrackLength = @(track)(numel(track));

% read tracks and mask
if(COUNTER)
    [tracks, ~] = readTracksFromJSON(counterTrackFileName);
    maskFile = load(counterMaskFileName);
    counterMask = maskFile.mask_2;
else
    [tracks, ~] = readTracksFromJSON(tableTrackFileName);
    maskFile = load(tableMaskFileName);
    counterMask = maskFile.table_mask;
end
fprintf("total number of tracks: %d\n", numel(tracks));

% track merging
if(MERGE_TRACK)
    tracks = MotionTrackMerging(tracks, probTresh, wienerVar);
end

% find tacks passes through conter area
passCounter = zeros(numel(tracks), 1);
for i = 1 : numel(tracks)
    track = tracks{i};
    for j = 1 : numel(track)
        detection = track{j};
        location = detection{1};
        if(counterMask(location(2), location(1)))
            % detected inside counter mask
            passCounter(i) = 1;
            break;
        end
    end
end
trackPassMask = tracks(passCounter == 1);
fprintf("number of tracks passing through counter: %d\n", numel(find(passCounter)));

% compute average dwelling time in counter area
dwellTimes = zeros(numel(trackPassMask), 1);
for i = 1 : numel(trackPassMask)
    track = trackPassMask{i};
    for j = 1 : numel(track)
        detection = track{j};
        location = detection{1};
        if(counterMask(location(2), location(1)))
            % detected inside counter mask
            dwellTimes(i) = dwellTimes(i) + 1;
        end
    end
end

figure(1);
trackLengths = cellfun(findTrackLength, tracks);
subplot(1, 3, 1); histogram(trackLengths, 10); title("Lengths of all tracks"); xlabel("Track Length");

% filter out short tracks
dwellTimes = dwellTimes(dwellTimes > minDwellTime);
passTrackLengths = cellfun(findTrackLength, trackPassMask);
subplot(1, 3, 2); histogram(passTrackLengths, 10); title("Lengths of tracks passing through mask"); xlabel("Track Length");
fprintf("number of longer tracks passing through mask: %d\n", numel(dwellTimes));

subplot(1, 3, 3); histogram(dwellTimes, 10); title("dwelling time for long tracks"); xlabel("Dwelling Time");
totalDwellTime = sum(dwellTimes);
avgDwellTime = totalDwellTime / numel(dwellTimes);
if(COUNTER)
    fprintf("Counter average dwell time: %.3f frames\n", avgDwellTime);
else
    fprintf("Table average dwell time: %.3f frames\n", avgDwellTime);
end