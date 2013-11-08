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
ycd1;  %list of y-coordinates for color 1
cmd2;  %list of commands for color 2
xcd2;  %list of x-coordinates for color 2
ycd2;  %list of y-coordinates for color 2
%}

%clear workspace
clear

%open the Python output file
pyOutFile = fopen('pythonOutput.txt');

%=================
% get color 0 info
%=================
%get commands
pyLine = fgetl(pyOutFile);  %get a line from the file
[pyLineDesc, pyLineData] = strtok(pyLine, '[');  %get bracketed info
pyLineData = strtok(pyLineData, '[]');  %remove brackets
pyLineData = strsplit(pyLineData, ',');  %remove commas
cmd0 = char(pyLineData);  %turn cell array (of strings) into a char array

%get x-coords
pyLine = fgetl(pyOutFile);  %get a line from the file
[pyLineDesc, pyLineData] = strtok(pyLine, '[');  %get bracketed info
pyLineData = strtok(pyLineData, '[]');  %remove brackets
xcd0 = str2num(pyLineData);  %turn string into numeric array
xcd0 = transpose(xcd0);  %it's easier to work with column vectors

%get y-coords
pyLine = fgetl(pyOutFile);  %get a line from the file
[pyLineDesc, pyLineData] = strtok(pyLine, '[');  %get bracketed info
pyLineData = strtok(pyLineData, '[]');  %remove brackets
ycd0 = str2num(pyLineData);  %turn string into numeric array
ycd0 = transpose(ycd0);  %it's easier to work with column vectors
ycd0 = -1.*ycd0;  %negate y-coords because our coord system is upside down


%=================
% get color 1 info
%=================
%get commands
pyLine = fgetl(pyOutFile);  %get a line from the file
[pyLineDesc, pyLineData] = strtok(pyLine, '[');  %get bracketed info
pyLineData = strtok(pyLineData, '[]');  %remove brackets
pyLineData = strsplit(pyLineData, ',');  %remove commas
cmd1 = char(pyLineData);  %turn cell array (of strings) into a char array

%get x-coords
pyLine = fgetl(pyOutFile);  %get a line from the file
[pyLineDesc, pyLineData] = strtok(pyLine, '[');  %get bracketed info
pyLineData = strtok(pyLineData, '[]');  %remove brackets
xcd1 = str2num(pyLineData);  %turn string into numeric array
xcd1 = transpose(xcd1);  %it's easier to work with column vectors

%get y-coords
pyLine = fgetl(pyOutFile);  %get a line from the file
[pyLineDesc, pyLineData] = strtok(pyLine, '[');  %get bracketed info
pyLineData = strtok(pyLineData, '[]');  %remove brackets
ycd1 = str2num(pyLineData);  %turn string into numeric array
ycd1 = transpose(ycd1);  %it's easier to work with column vectors
ycd1 = -1.*ycd1;  %negate y-coords because our coord system is upside down

%=================
% get color 2 info
%=================
%get commands
pyLine = fgetl(pyOutFile);  %get a line from the file
[pyLineDesc, pyLineData] = strtok(pyLine, '[');  %get bracketed info
pyLineData = strtok(pyLineData, '[]');  %remove brackets
pyLineData = strsplit(pyLineData, ',');  %remove commas
cmd2 = char(pyLineData);  %turn cell array (of strings) into a char array

%get x-coords
pyLine = fgetl(pyOutFile);  %get a line from the file
[pyLineDesc, pyLineData] = strtok(pyLine, '[');  %get bracketed info
pyLineData = strtok(pyLineData, '[]');  %remove brackets
xcd2 = str2num(pyLineData);  %turn string into numeric array
xcd2 = transpose(xcd2);  %it's easier to work with column vectors

%get y-coords
pyLine = fgetl(pyOutFile);  %get a line from the file
[pyLineDesc, pyLineData] = strtok(pyLine, '[');  %get bracketed info
pyLineData = strtok(pyLineData, '[]');  %remove brackets
ycd2 = str2num(pyLineData);  %turn string into numeric array
ycd2 = transpose(ycd2);  %it's easier to work with column vectors
ycd2 = -1.*ycd2;  %negate y-coords because our coord system is upside down


fclose(pyOutFile);

%=========================================
% three for-loops to plot the three colors
%=========================================
%for-loop for color 0
if length(cmd0) > 1
    for i=2:length(cmd0)
        if cmd0(i) == 'L'
            seg = plot([xcd0(i-1) xcd0(i)],[ycd0(i-1) ycd0(i)]);
            hold on;  %retain current graph while adding line segments
            set(seg,'Color',[0,0,.50]);  %dark blue
            set(seg,'LineWidth',10);  %default is 0.5
            %set(seg,'Marker','x');  %makes counting line segments easier
            xlim([0 744.09448]);
            ylim([-1052.3622 0]);
        end
    end
end

%for-loop for color 1
if length(cmd1) > 1
    for i=2:length(cmd1)
        if cmd1(i) == 'L'
            seg = plot([xcd1(i-1) xcd1(i)],[ycd1(i-1) ycd1(i)]);
            hold on;  %retain current graph while adding line segments
            set(seg,'Color',[.25,.41,.88]);  %light blue
            set(seg,'LineWidth',10);  %default is 0.5
            set(seg,'Marker','.');  %makes counting line segments easier
            xlim([0 744.09448]);
            ylim([-1052.3622 0]);
        end
    end
end

%for-loop for color 2
if length(cmd2) > 1
    for i=2:length(cmd2)
        if cmd2(i) == 'L'
            seg = plot([xcd2(i-1) xcd2(i)],[ycd2(i-1) ycd2(i)]);
            hold on;  %retain current graph while adding line segments
            set(seg,'Color',[1,.65,0]);  %burnt orange
            set(seg,'LineWidth',10);  %default is 0.5
            set(seg,'Marker','.');  %makes counting line segments easier
            xlim([0 744.09448]);
            ylim([-1052.3622 0]);
        end
    end
end


