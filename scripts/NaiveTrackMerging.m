function [mergedTracks, M] = NaiveTrackMerging(tracks, Pthresh, sigma2)
    [mergeables, M] = detectMergeableTracks(tracks, Pthresh, sigma2);
    mergedTracks = mergeTracks(tracks, mergeables);
end

function tracks = mergeTracks(tracks, mergeables)
    for i = 1 : size(mergeables, 1)
        m = mergeables(i, :);
        tp = tracks{m(1)};
        tq = tracks{m(2)};
        tracks{m(1)} = cat(1, tp, tq);
        tracks{m(2)} = [];
    end
end

function [mergeables, M] = detectMergeableTracks(tracks, Pthresh, sigma2)
    trackModels = convertTrackModel(tracks);
    P = zeros(numel(trackModels));
    for i = 1 : numel(trackModels)
        for j = 1 : numel(trackModels)
            if(i == j)
                P(i, j) = -inf;
                continue;
            end
            ti = trackModels{i};
            tj = trackModels{j};
            xei = ti.xe;
            xsj = tj.xs;
            tei = ti.te;
            tsj = tj.ts;
            %sigmat2 = sigma2;
            sigmat2 = abs(tsj-tei)*sigma2;
            P(i, j) = exp(-sum((xsj-xei).^2)/(2*sigmat2)) / (2*pi*sigmat2);
        end
    end
    M = P > Pthresh;
    [row, col, ~] = find(M);
    mergeables = [row, col];
end

function newTracks = convertTrackModel(tracks)
    newTracks = cell(numel(tracks), 1);
    for i = 1 : numel(newTracks)
        t = tracks{i};
        ds = t{1};
        de = t{end};
        track.xs = ds{1};
        track.ts = ds{2};
        track.xe = de{1};
        track.te = de{2};
        newTracks{i} = track;
    end
end