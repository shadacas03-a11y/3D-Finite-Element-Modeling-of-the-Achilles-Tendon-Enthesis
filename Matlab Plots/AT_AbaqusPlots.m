clear
clc
close all

%% Read CSV

T = readtable('C:\Users\CAMILA CASTRO\Downloads\Force_Displacement_ModelB1.csv')
time = T.Time;
U = T.Displacement_U3;
RF = abs(T.ReactionForce_Z);

%% --------------------------------------------------------
%% Force vs Displacement
%% --------------------------------------------------------

figure

plot(U,RF,'LineWidth',2)

grid on
box on

xlabel('Displacement (mm)')
ylabel('Reaction Force (N)')
title('Force-Displacement Curve')

%% --------------------------------------------------------
%% Force vs Time
%% --------------------------------------------------------

figure

plot(time,RF,'LineWidth',2)

grid on
box on

xlabel('Time')
ylabel('Reaction Force (N)')
title('Reaction Force')

%% --------------------------------------------------------
%% Displacement vs Time
%% --------------------------------------------------------

figure

plot(time,U,'LineWidth',2)

grid on
box on

xlabel('Time')
ylabel('Displacement (mm)')
title('Displacement')

%% --------------------------------------------------------
%% Tangent stiffness
%% --------------------------------------------------------

k = gradient(RF)./gradient(U);

figure

plot(U,k,'LineWidth',2)

grid on
box on

xlabel('Displacement (mm)')
ylabel('Stiffness (N/mm)')
title('Instantaneous Stiffness')

%% --------------------------------------------------------
%% Strain Energy
%% --------------------------------------------------------

Energy = trapz(U,RF);

fprintf('\n');
fprintf('---------------------------------\n');
fprintf('Strain Energy = %.3f N.mm\n',Energy);
fprintf('---------------------------------\n');

