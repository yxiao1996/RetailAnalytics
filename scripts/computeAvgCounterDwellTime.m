% filenames
trackFileName = "YOLO2DSSqrNMSTracks.json";
maskFileName = "counter_mask_large.mat";

% parameters
minTrackLen = 100;

% handles
findTrackLength = @(track)(numel(track));

% read tracks and mask
[tracks, ~] = readTracksFromJSON(trackFileName);
maskFile = load(maskFileName);
counterMask = maskFile.mask_2;
fprintf("total number of tracks: %d\n", numel(tracks));

% find tacks passes through conter area
passCounter = zeros(numel(tracks), 1);
for i = 1 : numel(tracks)
    track = tracks{i};
    for j = 1 : numel(track)
        detection = track{j};
        location = detection{1};
        if(counterMask(location(1), location(2)))
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
subplot(1, 2, 1); histogram(trackLengths); title("Lengths of all tracks");
passTrackLengths = cellfun(findTrackLength, tracksPassCounter);
subplot(1, 2, 2); histogram(passTrackLengths); title("Lengths of tracks passing through counter");

% filter out short tracks
tracksPassCounter = tracksPassCounter(passTrackLengths > minTrackLen);
fprintf("number of longer tracks passing through counter: %d\n", numel(tracksPassCounter));

% compute average dwelling time in counter area
totalDwellTime = 0;
for i = 1 : numel(tracksPassCounter)
    track = tracksPassCounter{i};
    for j = 1 : numel(track)
        detection = track{j};
        location = detection{1};
        if(counterMask(location(1), location(2)))
            % detected inside counter mask
            totalDwellTime = totalDwellTime + 1;
        end
    end
end
avgDwellTime = totalDwellTime / numel(tracksPassCounter);
fprintf("average dwell time: %.3f frames\n", avgDwellTime);