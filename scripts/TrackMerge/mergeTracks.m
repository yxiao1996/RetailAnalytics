function tracks = mergeTracks(tracks, mergeables)   
    groups = findMergeGroups(mergeables);
    for i = 1 : numel(groups)
        idxGroup = unique(cell2mat(groups{i}));
        tracks{idxGroup(1)} = cat(1, tracks{idxGroup});
        for j = 2 : numel(idxGroup)
            tracks{idxGroup(j)} = [];
        end
    end
end

function groups = findMergeGroups(mergeables)
    groups = {};
    for i = 1 : size(mergeables, 1)
        inGroup = false;
        mergeable = mergeables(i, :);
        for j = 1 : numel(groups)
            group = groups{j};
            if(ismember(mergeable(1), cell2mat(group)) || ...
               ismember(mergeable(2), cell2mat(group)))
                inGroup = true;
                group{numel(group)+1} = mergeable;
                groups{j} = group;
            end
        end
        if(~inGroup)
            groups{numel(groups)+1} = {mergeable};
        end
    end
end