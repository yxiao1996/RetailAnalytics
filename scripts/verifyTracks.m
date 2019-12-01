minTrackLength = 40;

scene = imread("frame0000.jpg");
fid = fopen('trakcs.json');
trackStruct = jsondecode(char(fread(fid, inf)'));
fclose(fid);

trackNames = fieldnames(trackStruct);
tracks = cell(numel(trackNames), 1);

for i = 1 : numel(trackNames)
    tracks{i} = trackStruct.(trackNames{i});
end

% filter out very short tracks
findTrackLength = @(track)(numel(track));
trackLengths = cellfun(findTrackLength, tracks);
tracks = tracks(trackLengths > minTrackLength);

startPoints = zeros(numel(tracks), 2);
for i = 1 : numel(tracks)
    track = tracks{i};
    startPointInfo = track{1};
    startPoints(i, :) = startPointInfo{1};
end

imshow(insertMarker(scene, startPoints, 'Size', 6));