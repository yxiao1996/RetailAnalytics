% filenames
trackFileName = "YOLO2DSNMSTracks.json";
maskFileName = "table_mask.mat";

% parameters
minTrackLen = 150;

% handles
findTrackLength = @(track)(numel(track));

% read tracks and mask
[tracks, ~] = readTracksFromJSON(trackFileName);
maskFile = load(maskFileName);
counterMask = maskFile.table_mask;
fprintf("total number of tracks: %d\n", numel(tracks));

% track merging
tracks = NaiveTrackMerging(tracks, 0.0001, 1);

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
tracksPassCounter = tracks(passCounter == 1);
fprintf("number of tracks passing through counter: %d\n", numel(find(passCounter)));

figure(1);
findTrackLength = @(track)(numel(track));
trackLengths = cellfun(findTrackLength, tracks);
subplot(1, 3, 1); histogram(trackLengths); title("Lengths of all tracks"); xlabel("Track Length");
passTrackLengths = cellfun(findTrackLength, tracksPassCounter);
subplot(1, 3, 2); histogram(passTrackLengths); title("Lengths of tracks passing through counter"); xlabel("Track Length");

% filter out short tracks
tracksPassCounter = tracksPassCounter(passTrackLengths > minTrackLen);
fprintf("number of longer tracks passing through counter: %d\n", numel(tracksPassCounter));

% compute average dwelling time in counter area
dwellTimes = zeros(numel(tracksPassCounter), 1);
for i = 1 : numel(tracksPassCounter)
    track = tracksPassCounter{i};
    for j = 1 : numel(track)
        detection = track{j};
        location = detection{1};
        if(counterMask(location(2), location(1)))
            % detected inside counter mask
            dwellTimes(i) = dwellTimes(i) + 1;
        end
    end
end
subplot(1, 3, 3); histogram(dwellTimes, 10); title("dwelling time for long tracks"); xlabel("Dwelling Time");
totalDwellTime = sum(dwellTimes);
avgDwellTime = totalDwellTime / numel(tracksPassCounter);
fprintf("average dwell time: %.3f frames\n", avgDwellTime);