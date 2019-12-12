xlimit = [0 10];
ylimit = [0 10];
tEnd = 20;
nTrack = 10;

% generate random tracks
tracks = cell(nTrack, 1);
for i = 1 : nTrack
    startPoint = rand(2, 1) .* [xlimit(2); ylimit(2)];
    endPoint = rand(2, 1) .* [xlimit(2); ylimit(2)];
    midPoints = [
        (0:tEnd)*(endPoint(1)-startPoint(1))/tEnd+startPoint(1); ...
        (0:tEnd)*(endPoint(2)-startPoint(2))/tEnd+startPoint(2)
    ]';
    track = cell(tEnd+1, 1);
    for j = 0 : tEnd
        track{j+1} = {midPoints(j+1, :)'; j};
    end
    tracks{i} = track;
end
plotTrack(tracks);

% randomly break the track
for i = 1 : nTrack
    rt = floor(rand*tEnd/2)+tEnd/4;
    rd = floor(rand*2)+2;
    track = tracks{i};
    tracks{i} = {track{1:rt-floor(rd/2)}}';
    tracks{i+nTrack} = {track{rt+floor(rd/2)+1:end}}';
end
plotTrack(tracks);

% merge track
%tracks = NaiveTrackMerging(tracks, 0.05, 0.3);
tracks = MotionTrackMerging(tracks, 1, 0.01);
plotTrack(tracks);

function plotTrack(tracks)   
    figure();
    for i = 1 : numel(tracks)
        track = tracks{i};
        if(numel(track) == 0)
            continue
        end
        t = cell2mat(cellfun(@(d)(d{2}), track, 'UniformOutput', false));
        xy = cell2mat(cellfun(@(d)(d{1}'), track, 'UniformOutput', false));
        plot3(t, xy(:,1),xy(:,2),'-o','MarkerSize',10,'MarkerFaceColor','#D9FFFF');
        hold on;
    end
    xlabel("t"); ylabel("x"); zlabel("y");
    grid on;
    view(-10,20)
end