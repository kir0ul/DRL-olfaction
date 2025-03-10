function plot_distribution(X,Y,color_value)
% PLOT_DISTRIBUTION(X,Y) - Plots the mean with standard deviation errors as a shaded region in the open 
% figure window.
% Inputs:
%     X: vector of n domain values (the x-axis).
%     Y: mxn matrix of distribution of range values (the y-axis), where m 
%           corresponds to the number of data samples for each value n.
%
% PLOT_DISTRIBUTION(X,Y,...)
% Parameter options include:
%     'Alpha': the alpha value of the shaded region, default 0.15.
%     'Color': the shaded region color.
%     'LineWidth': the contour line width, default = 2.0.

alpha_value =0.15;
line_width = 2.0;

MU = mean(Y);
SIGMA = std(Y);
hold on
% Create the polygons for the shaded region
Ptop = MU+SIGMA;
Pbot = MU-SIGMA;
for i=1:numel(X)-1
    Px = [X(i) X(i+1) X(i+1) X(i)];
    Py = [Ptop(i) Ptop(i+1) Pbot(i+1) Pbot(i)];
    fill(Px,Py,color_value,'FaceAlpha',alpha_value,'EdgeColor','none');
end
plot(X,MU,'LineWidth',line_width,'Color',color_value);
hold off
end
