function [tracks, trackNames] = readTracksFromJSON(fileName)
    trackStruct = jsondecode(fileread(fileName));

    trackNames = fieldnames(trackStruct);
    tracks = cell(numel(trackNames), 1);

    for i = 1 : numel(trackNames)
        tracks{i} = trackStruct.(trackNames{i});
    end
end

