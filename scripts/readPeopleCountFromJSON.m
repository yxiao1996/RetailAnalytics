fileName = "peopleCountMRCNNTrackMask.json";

count = cellfun(@(countStr)(str2double(countStr)), jsondecode(fileread(fileName)));
countEntropy = entropy(count/max(abs(count)));

labelFile = load("labels.mat");
labels = labelFile.labels;
labelEntropy = entropy(labels/max(abs(labels)));

diff = labels - count;
diffEntropy = entropy((diff-min(diff))/max(abs(diff-min(diff))));

plot(1:numel(labels), labels, 1:numel(count), count);
legend("Count Label", "Count Prediction");
axis([1 numel(count) 0 35]);
title(strcat("people count in file ", fileName, sprintf(", Prediction Entropy: %.3f, Label Entropy: %.3f, Diff Entropy %.3f", countEntropy, labelEntropy, diffEntropy)));