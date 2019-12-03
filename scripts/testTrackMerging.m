trackFileName = "MRCNNDSCam42Trakcs.json";
labelFile = load("mrcnnMergeLabel1");
label = labelFile.mergeable;
[tracks, trackNames] = readTracksFromJSON(trackFileName);

npoints = 20;
maxExp = 6;
curv = zeros(npoints, 2);
vars = 0.1.^(1:4);
for j = 1 : numel(vars)
    for i = 1 : npoints
        thresh = 0.1^(maxExp*i*(1/npoints));
        [~, M] = NaiveTrackMerging(tracks, thresh, vars(j));
        recall = sum(double(M(label == 1))) / numel(find(label));
        ccr = numel(find(double(M) == label)) / numel(label);
        fpr = sum(double(M(label == 0))) / (numel(label) - numel(find(label)));
        curv(i, :) = [fpr recall];
        disp(i);
    end
    plot(curv(:, 1), curv(:, 2)); hold on
end

legend(arrayfun(@(v)({num2str(v)}), vars))