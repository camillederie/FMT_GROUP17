clc; clear all; close all; 
addpath(genpath('testdata')); 

%%  Config
urange = 0:2:20; 
fileName = './Group17/Calibration_%03d.txt'; 

for ii = 1:numel(urange)
    fileIn = sprintf(fileName,urange(ii));     
    delimiter = ' ';
    startRow = 23;
    formatSpec = '%s';
    try
        fileID = fopen(fileIn,'r');
    catch
        fileID = fopen(fileIn{1},'r');
    end
    tmp = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'TextType', 'string', 'HeaderLines' ,startRow, 'ReturnOnError', false, 'EndOfLine', '\r\n');
    fclose(fileID);
    tmp2 = strrep(tmp{1},',','.');
    
    fileOut = strcat(fileIn,'_mat');
    fileId = fopen(fileOut,'w');
    fprintf(fileId, '%s\n', tmp2);
    fclose(fileID);
    
    
    data  = dlmread(fileOut); 
    u(ii) = mean(data(:,2));
end

%%  Fit Poly
x = u; 
xplot = linspace(x(1),x(end),100); 
y = urange; 
c = polyfit(x,y,4); 

figure(1); clf; set(gcf,'color','w','position',[381 558 859 420]); 
plot(y,x,'k.','markersize',10); 
hold on; 
plot(polyval(c,xplot),xplot)
xlabel('u [m/s]'); ylabel('E [V]'); 
set(gca,'fontsize',14)

% dim = [.2 .5 .3 .3];
str = 'u = (%2.2f) E^4 + (%2.2f) E^3 + (%2.2f) E^2 + (%2.2f) E + (%2.2f)';
% annotation('textbox',dim,'String',sprintf(str,c),'FitBoxToText','on');
title(sprintf(str,c))
