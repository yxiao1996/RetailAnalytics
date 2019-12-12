function [mergedTracks, M] = MotionTrackMerging(tracks, Pthresh, sigma2)
    [mergeables, M] = detectMergeableTracks(tracks, Pthresh, sigma2);
    mergedTracks = mergeTracks(tracks, mergeables);
end

function [mergeables, M] = detectMergeableTracks(tracks, Pthresh, sigma2)
    trackModels = convertTrackModel(tracks);
    P = zeros(numel(trackModels));
    for i = 1 : numel(trackModels)
        for j = 1 : numel(trackModels)           
            ti = trackModels{i};
            tj = trackModels{j};
            xei = ti.xe;
            xsj = tj.xs;
            tei = ti.te;
            tsj = tj.ts;
            if(tei >= tsj)
                P(i, j) = -inf;
                continue;
            end
            v = ti.v;
            xsjHat = xei + v*(tsj-tei); % estimate xsj
            sigmat2 = abs(tsj-tei)*sigma2;
            P(i, j) = exp(-sum((xsj-xsjHat).^2)/(2*sigmat2)) / (2*pi*sigmat2);
        end
    end
    M = P > Pthresh;
    [row, col, ~] = find(M);
    mergeables = [row, col];
end

function newTracks = convertTrackModel(tracks)
    newTracks = cell(numel(tracks), 1);
    for i = 1 : numel(newTracks)
        tk = tracks{i};
        ds = tk{1};
        de = tk{end};
        track.xs = ds{1};
        track.ts = ds{2};
        track.xe = de{1};
        track.te = de{2};
        % compute linear velocity
        xy = cell2mat(cellfun(@(d)(d{1}'), tk, 'UniformOutput', false));
        t = cell2mat(cellfun(@(d)(d{2}), tk, 'UniformOutput', false));
        [vx, vy] = computeVelocity(xy, t);
        track.v = [vx; vy];
        newTracks{i} = track;
    end
end

function [vx, vy] = computeVelocity(xy, t)
    xyNorm = xy - xy(1, :);
    vx = sum(t .* xyNorm(:, 1)) / sum(t .* t);
    vy = sum(t .* xyNorm(:, 2)) / sum(t .* t);
end