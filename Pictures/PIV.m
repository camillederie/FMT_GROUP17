% Clear the workspace and variables
clc;
clear all;
close all;

dt = 75 * 10^-6; % Pulse interval
pixel_width = 0.17 / 1628; % Pixel width = x_FOV/x_resolution

% Read TIF Image Data
% Create a Tif object and read data from the TIF file

Vxs = {};
Vys = {};
Vs = {};

for n = 1:9
    t = imread('B0000' + string(n), 'tif');

    % Read the size of the actual image
    [xmax, ymax] = size(t);

    % Split the image in two
    t_a = t(1:xmax/2, :);
    t_b = t(xmax/2+1:end, :);

    % Read the size of the new images
    [xmax, ymax] = size(t_a);

    % Window size (should be selected appropriately)
    wsize = [32, 32];
    % Overlap [%]
    woverlap = 0.5;

    w_width = wsize(1);
    w_height = wsize(2);

    % Define windows all over the domain
    xmin = w_width / 2;
    ymin = w_height / 2;

    % Array for x co-ordinate of all the windows
    xgrid = w_width * 2 : w_width * woverlap : xmax - w_width * 2;

    % Array for y co-ordinate of all the windows
    ygrid = w_height * 2 : w_height * woverlap : ymax - w_height * 2;

    % Range of 'search' windows in image 2
    w_xcount = length(xgrid);
    w_ycount = length(ygrid);

    % For every window we have to create the test matrix in image 1. 
    % Then in image 2, we have to correlate this test window around 
    % its original position in image 1, the range is predetermined.
    % The point of max correlation corresponds to the final average 
    % displacement of that window.
    x_disp_max = w_width / 2;
    y_disp_max = w_height / 2;

    test_ima(w_width, w_height) = 0;
    test_imb(w_width + 2 * x_disp_max, w_height + 2 * y_disp_max) = 0;

    % Initialise x and y direction displacement
    dpx(w_xcount, w_ycount) = 0;
    dpy(w_xcount, w_ycount) = 0;

    xpeak1 = 0;
    ypeak1 = 0;

    % Using for loop to investigate each window.
    % i, j for the windows
    % test_i and test_j are for the test window to be 
    % extracted from image 1.
    for i = 1:w_xcount
        for j = 1:w_ycount
            max_correlation = 0;
            test_xmin = xgrid(i) - w_width * woverlap;       % left x co-ordinate
            test_xmax = xgrid(i) + w_width * woverlap;       % right x co-ordinate
            test_ymin = ygrid(j) - w_height * woverlap;      % bottom y co-ordinate
            test_ymax = ygrid(j) + w_height * woverlap;      % top y co-ordinate

            x_disp = 0;
            y_disp = 0;

            % Windows of image 1 and image 2
            test_ima = t_a(test_xmin:test_xmax, test_ymin:test_ymax);
            test_imb = t_b((test_xmin - x_disp_max):(test_xmax + x_disp_max), (test_ymin - y_disp_max):(test_ymax + y_disp_max));

            % Calculate the correlation
            correlation = normxcorr2(test_ima, test_imb);
            [ypeak, xpeak] = find(correlation == max(correlation(:)));

            % Re-scaling
            xpeak1 = test_xmin + xpeak - wsize(1) * woverlap - x_disp_max;
            ypeak1 = test_ymin + ypeak - wsize(2) * woverlap - y_disp_max;
            dpx(i, j) = xpeak1 - xgrid(i);
            dpy(i, j) = ypeak1 - ygrid(j);
        end
    end

    % Convert to physical values
    Vx = dpx .* pixel_width / dt;
    Vy = dpy .* pixel_width / dt;

    % Filter out non-physical values per set limit
    V_x_max = 15;
    V_x_min = -5;
    V_y_max = 5;
    V_y_min = -5;

    for i = 1:length(Vx(1, :))
        for j = 1:length(Vx(:, 1))
            if Vx(j, i) > V_x_max || abs(Vy(j, i)) > V_y_max || Vx(j, i) < V_x_min || abs(Vy(j, i)) < V_y_min
                Vx(j, i) = 0;
                Vy(j, i) = 0;
            end
        end
    end

    % Calculate velocity magnitude
    V = sqrt(Vx.^2 + Vy.^2);

    Vxs{n} = Vx;
    Vys{n} = Vy;
    Vs{n} = V;
end


%ensemble averaging

stacked_Vxs = cat(3, Vxs{:});
stacked_Vys = cat(3, Vys{:});
stacked_Vs = cat(3, Vs{:});

% %Trimmean to filter out outliers from mean computation
Vx_a = trimmean(stacked_Vxs,95, 3);
Vy_a = trimmean(stacked_Vys,95, 3);
V_a = trimmean(stacked_Vs,95, 3);

% Display results
figure;

% Display the magnitude of the velocity as a background image
imagesc(flip(V_a));
c = colorbar; % Add a colorbar to indicate the scale
colormap(jet); % Apply the 'jet' colormap
c.Label.String = 'Velocity Magnitude [m/s]'; % Add title to the colorbar
hold on;

% Overlay the vector field on top
[x, y] = meshgrid(1:size(Vx, 2), 1:size(Vx, 1)); % Create a grid for the vectors
quiver(x, y, flip(Vx_a), flip(Vy_a), 'k'); % Plot the vector field with black arrows
