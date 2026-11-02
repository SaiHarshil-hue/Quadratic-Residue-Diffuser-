function plot_depths(csvFile, pngFile)
% PLOT_DEPTHS  Bar graph of calculated well depths.
%   MATLAB is used ONLY for plotting. All calculations are done in Python.
%
%   plot_depths(csvFile, pngFile) reads the CSV file written by Python and
%   saves a bar graph (well number vs depth in cm) as a PNG image.
%
%   plot_depths() uses the default files:
%       ..\data\results.csv  ->  ..\graphs\depths.png
%
%   Example (from inside the matlab folder):
%       plot_depths('..\data\results.csv', '..\graphs\depths.png')

    % ---- default file names (relative to this script's folder) ----
    here = fileparts(mfilename('fullpath'));
    if nargin < 1
        csvFile = fullfile(here, '..', 'data', 'results.csv');
    end
    if nargin < 2
        pngFile = fullfile(here, '..', 'graphs', 'depths.png');
    end

    % ---- read and check the data ----
    if ~isfile(csvFile)
        error('CSV file not found: %s', csvFile);
    end
    T = readtable(csvFile);
    names = T.Properties.VariableNames;
    if ~all(ismember({'Well', 'Depth_cm'}, names))
        error('CSV must contain the columns Well and Depth_cm.');
    end
    wells  = T.Well;
    depths = T.Depth_cm;
    if isempty(wells) || numel(wells) ~= numel(depths)
        error('Well and Depth_cm must be non-empty and have the same length.');
    end

    % ---- make the bar graph (figure is not shown on screen) ----
    fig = figure('Visible', 'off', 'Color', 'w');
    bar(wells, depths);
    grid on;
    if numel(wells) <= 30
        xticks(wells);
    end
    xlabel('Well number (n)');
    ylabel('Well depth (cm)');
    title({sprintf('Calculated Well Depths (p = %d wells)', numel(wells)), ...
           'Calculated values from a simplified model - not measured acoustic performance'});

    % ---- save as PNG ----
    outFolder = fileparts(pngFile);
    if ~isempty(outFolder) && ~isfolder(outFolder)
        mkdir(outFolder);
    end
    if exist('exportgraphics', 'file')
        exportgraphics(fig, pngFile, 'Resolution', 200);
    else
        saveas(fig, pngFile);
    end
    close(fig);
    fprintf('Graph saved to: %s\n', pngFile);
end
