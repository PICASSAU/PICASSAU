% Coordinate Plotting Simulation for
% PICASSAU, the Painting Robot
% a Senior Design Project by
% Ben Straub, David Toledo, Drew Kerr, Kayla Frost, and Peter Gartland
% 6 Oct. 2013

% This MATLAB script will read a file containing the coordinates and move
% commands used by PICASSAU and will generate a plot, so we can see what
% PICASSAU is about to paint.

%{
% define some useful variables, arrays, etc.
cmd0;  %list of commands for color 0
xcd0;  %list of x-coordinates for color 0
ycd0;  %list of y-coordinates for color 0
cmd1;  %list of commands for color 1
xcd1;  %list of x-coordinates for color 1
ycd0;  %list of y-coordinates for color 1
cmd2;  %list of commands for color 2
xcd0;  %list of x-coordinates for color 2
ycd0;  %list of y-coordinates for color 2
%}

%clear workspace
clear

%open the Python output file
pyOutFile = fopen('pythonOutput.txt');

%=================
% get color 0 info
%=================
%extract color 0 commands
pyLine = fgetl(pyOutFile);  %get a line from the file
pyLineData = strtok(pyLineData, '[]');  %get everything inside the brackets, [...]
data = strsplit(pyLineData, ',');  %get data from in between commas
cmd0 = char(data);  %convert cell array (of strings) into a character array

%{
pyLineDatum = sscanf(pyLineData, '%c');  %look at one charcter at a time
while pyLineDatum ~= ']'
    if pyLineDatum ~= ','
        cmd0(i) = pyLineDatum;
    end
    i = i + 1;
    pyLineDatum = sscanf(pyLineData, '%c');  %get the next character
end

%extract color 0 x-coords
pyLine = fgetl(pyOutFile)
lineDesc = sscanf(pyLine, '%s')
[xcd0, xcd0_size] = sscanf(pyLine, '%d')

%extract color 0 y-coords


	
%=================
% get color 1 info
%=================
pyLine = fgetl(pyOutFile);
%extract color 1 commands

pyLine = fgetl(pyOutFile);
%extract color 1 x-coords

pyLine = fgetl(pyOutFile);
%extract color 1 y-coords



%=================
% get color 2 info
%=================
pyLine = fgetl(pyOutFile);
%extract color 2 commands

pyLine = fgetl(pyOutFile);
%extract color 2 x-coords

pyLine = fgetl(pyOutFile);
%extract color 2 y-coords



%three for-loops to plot the three colors
%for-loop for color 0


%for-loop for color 1


%for-loop for color 2


%}