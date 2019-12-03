trackFileName = "MRCNNDSCam42Trakcs.json";

[tracks, trackNames] = readTracksFromJSON(trackFileName);

%mergeable = zeros(numel(tracks));

while true
    i = input('track i = ');
    j = input('track j = ');
    [~, ii] = ismember(strcat('x', num2str(i)), trackNames);
    [~, jj] = ismember(strcat('x', num2str(j)), trackNames);
    mergeable(ii, jj) = 1;
end