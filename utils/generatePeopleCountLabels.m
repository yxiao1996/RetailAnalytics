initialCount = 20;
labels = initialCount * ones(2001, 1);
indices = [18 20 100 204 243 348 625 669 682 940 950 955 1010 1378 1393 1464 1478 1500 1600 1691 1842 1877 1920 1991];
values  = [ 1  1   1   1  -1  -1   1  -1   1  -1   1  -1   -2    1   -1   -1   -1   -1    1    1   -1    1    1    1];
offset = 0;
for i = 2 : numel(indices)
    offset = offset + values(i-1);
    labels(indices(i-1)+1 : indices(i)) =  labels(indices(i-1)+1 : indices(i)) + offset;
end
plot(1:numel(labels), labels);