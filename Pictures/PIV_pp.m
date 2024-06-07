% clear the workspace and variables
clc
clear all
close all

dt = 75*10^-6; %Pulse interval
pixel_width = 0.15/1628; %


% Read TIF Image Data
% Create a Tif object and read data from the TIF file

t = imread('B00004', 'tif');

% read the size of the actual image
[xmax,ymax] = size(t);

% % Display the original image
% figure;
% imshow(t);
% title('Original Image (RGB)');

% % Display the contrast-enhanced image
% figure;
% imshow(t);
% title('Image');

%Split the image in two

t_a = t(1:xmax/2,:);
t_b = t(xmax/2+1:end,:);


% % Increase the contrast of the images
% % Adjust the image intensity values using imadjust
t_enhanced_a = imadjust(t_a);
t_enhanced_b = imadjust(t_b);

% 
% Display the splitted images in the same window
figure;

% Display the top half of the image
subplot(2, 1, 1); % Create a 2x1 grid, and place this image in the 1st part
imshow(t_enhanced_a);
title('Top Half of the Image (RGB)');

% Display the bottom half of the image
subplot(2, 1, 2); % Create a 2x1 grid, and place this image in the 2nd part
imshow(t_enhanced_b);
title('Bottom Half of the Image (RGB)');


% read the size of the new images
[xmax,ymax] = size(t_a);

% window size (should be selected appropriately)
wsize = [32,32];
w_width = wsize(1);
w_height = wsize(2);

% define windows all over the domain
xmin = w_width/2;
ymin = w_height/2;

% array for x co-ordinate of all the windows
xgrid = w_width*2:w_width/2:xmax-w_width*2;

% array for y co-ordinate of all the windows
ygrid = w_height*2:w_height/2:ymax-w_height*2;

% Range of 'search' windows in image 2
w_xcount = length(xgrid);
w_ycount = length(ygrid);


% For every window we have to create the test matrix in image 1. 
% Then in image 2, we have to corrrelate this test window around 
% its original position in image 1, the range is predetermined.
% The point of max correlation corresponds to the final average 
% displacement of that window.

x_disp_max = w_width/2;
y_disp_max = w_height/2;

test_ima(w_width,w_height) = 0;
test_imb(w_width+2*x_disp_max,w_height+2*y_disp_max) = 0;

% initialise x and y direction displacement
dpx(w_xcount,w_ycount) = 0;
dpy(w_xcount,w_ycount) = 0;


xpeak1=0;
ypeak1=0;

% using for loop to investigate each window.
% i,j for the windows
% test_i and test_j are for the test window to be 
% extracted from image 1.
for i=1:(w_xcount)
    
    for j=1:(w_ycount)
        
        max_correlation = 0;
        test_xmin = xgrid(i) - w_width/2;       % left x co-ordinate
        test_xmax = xgrid(i) + w_width/2;       % right x co-ordinate
        test_ymin = ygrid(j) - w_height/2;      % bottom y co-ordinate
        test_ymax = ygrid(j) + w_height/2;      % top y co-ordinate
        
        x_disp=0;
        y_disp=0;
        
        
        % windows of image 1 and image 2
        test_ima = t_a( test_xmin:test_xmax,test_ymin:test_ymax);
        test_imb = t_b( (test_xmin-x_disp_max):(test_xmax+x_disp_max),(test_ymin-y_disp_max):(test_ymax+y_disp_max));
        
        % calculate the correlation
        correlation = normxcorr2(test_ima,test_imb);
        [xpeak,ypeak] = find(correlation == max(correlation(:)));
        
        % Re-scaling
        xpeak1 = test_xmin+ xpeak - wsize(1)/2 - x_disp_max;
        ypeak1 = test_ymin+ ypeak - wsize(2)/2 - y_disp_max;
        dpx(i,j) = xpeak1-xgrid(i);
        dpy(i,j) = ypeak1-ygrid(j);
        
    end
    
end


%Convert to physical values

Vx = dpx.*pixel_width/dt;
Vy = dpy.*pixel_width/dt;


% display vector plot

figure;
quiver(dpy,-dpx)

figure;
quiver(Vy,-Vx)

average_dpx = mean2(dpx);
avergae_dpy = mean2 (dpy);


average_Vx = mean2(Vx);
avergae_Vy = mean2 (Vy);




