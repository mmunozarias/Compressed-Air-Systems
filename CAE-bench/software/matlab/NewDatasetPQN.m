clc
clear

% Open the serial port (adjust the COM port and baud rate accordingly)
s = serial('/dev/cu.usbmodem14101', 'BaudRate', 19200);

% Close any existing open connections on COM3
openConnections = instrfind('Port', '/dev/cu.usbmodem14101', 'Status', 'open');
if ~isempty(openConnections)
    fclose(openConnections);
end
fopen(s);


%Outliers parameters
window_size = 10;
outlier_threshold = 400;
outlier_pressure_threshold = 0.2;
outlier_flow_threshold = 400;

% Initialize variables
triggers = 0;
triggerAngle = 0;
previousValue = 0;
timeElapsed = 0;
intRPM = 0;
Angle = 0;
oldRPM = 0;
RPM_values = []; 
time_values = []; 
error_values = [];
output_values = [];
angle_values = [];  
pressure_values = [];
triggerFirstRun = 0;
previousAvgError = 0;
olderror = 0;
previousIntegral = 0;

currentAVGRPMvec = [];
AvgError = 0;
AvgError_values = [];
output = 0;
Proportional = 0;
Integral = 0;
Derivative = 0;
output_valuesD = [];
output_valuesI = [];
output_valuesP = [];
data = [];

RPM_plotted = [];
flow_plotted = [];
pressure_plotted = [];
time_values_plotted = [];

flow_values = [];


% Start measuring time
tic;

% Create the initial plot
% RPM plot
figure;

subplot(3, 1, 1);
h1 = plot(0, 0); % Create initial plot for RPM
ylabel('RPM');
hold on;

% Flow plot
subplot(3, 1, 2);
h3 = plot(0, 0, 'Color', 'r'); % Create initial plot for Flow
ylabel('Flow (L/Hour)');
hold on;

% Pressure plot
subplot(3, 1, 3);
h2 = plot(0, 0, 'Color', 'k'); % Create initial plot for Pressure
ylabel('Pressure (Bar)');
xlabel('Time (s)');
hold on;


% Main loop for real-time plotting
while timeElasped < 10
    drawnow;    
    % Read the trigger value from Arduino
    rawValue = fscanf(s, '%d,%f,%f');
    rawValue = [rawValue; timeElapsed];
    data = [data; rawValue'];
    rawValue = data(end,1);
    %rawFlow = data(:,3);
    
    
    % Check if the input from Arduino is 0 or 1
    if rawValue == 0 || rawValue == 1
        currentValue = rawValue;
    end

    % Check for trigger (transition from 1 to 0)
    if currentValue == 0 && previousValue == 1
        triggers = triggers + 1;
        triggerAngle = triggerAngle + 1;
        triggerFirstRun = triggerFirstRun + 1;

        % Calculate RPM every three triggers
        if triggers == 1
            % Measure the time elapsed since the last full rotation
            elapsedTime = toc;
            
            % Calculate RPM
            RPM = 60 / elapsedTime;

            % Update RPM values array
            RPM_values = [RPM_values, RPM];

            flownumbers = find(data(:,4) == timeElapsed);
            %flow = sum(data(flownumbers,3))/length(flownumbers);
            flow = sum(data(flownumbers,3))/elapsedTime;
            flow_rate = (flow/11) * 60; %flowrate L/hour

            flow_values = [flow_values, flow_rate];



       
            if length(flow_values) > window_size
                flow_filtered = movmean(flow_values(end-window_size+1:end), window_size);
            else
                flow_filtered = flow; %Setting first run to zero
            end
            outliers = abs(flow_values(end) - flow_filtered(end)) > outlier_flow_threshold;
            flow_values(end) = flow_filtered(end);


            pressure = data(end,2);
            pressure_values = [pressure_values, pressure];

            %Filering pressure values
            if length(pressure_values) > window_size
                pressure_filtered = movmean(pressure_values(end-window_size+1:end), window_size);
            else
                pressure_filtered = pressure; %Setting first run to zero
            end
            
            % Identify and replace outliers
            outliers = abs(pressure_values(end) - pressure_filtered(end)) > outlier_pressure_threshold;
            pressure_values(end) = pressure_filtered(end);

            %Filering RPM values
            if length(RPM_values) > window_size
                RPM_filtered = movmean(RPM_values(end-window_size+1:end), window_size);
                %RPM_plotting = 1000000;
            else
                RPM_filtered = RPM; %Setting first run to zero
                %RPM_plotting = 0;
            end
            
            % Identify and replace outliers
            outliers = abs(RPM_values(end) - RPM_filtered(end)) > outlier_threshold;
            RPM_values(end) = RPM_filtered(end);

            %RPM_plot_used = min(RPM_plotting,RPM_filtered);
            %RPM_plotted = [RPM_plotted, RPM_plot_used];



            % Update cumulative time values array
            timeElapsed = timeElapsed + elapsedTime;
            time_values = [time_values, timeElapsed];


            % Reset variables for the next full rotation
            triggers = 0;

            %Calcule PID control values
            %intRPM = intRPM + RPM * elapsedTime;
           
            % Calculate PID output
            %output = Kp * error + Kd * dRPMdt + Ki * intRPM;

            RPM_plotted = RPM_values;
            RPM_plotted(1:window_size) = 0;


            flow_plotted = flow_values;
            flow_plotted(1:window_size) = 0;

            pressure_plotted = pressure_values;
            pressure_plotted(1:window_size) = 0;

            set(h1, 'XData', time_values, 'YData', RPM_plotted); % Update RPM plot
            set(h3, 'XData', time_values, 'YData', flow_plotted); % Update Flow plot
            set(h2, 'XData', time_values, 'YData', pressure_plotted); % Update Pressure plot


            tic; % Start measuring time again
            %oldRPM = RPM;
            % previousIntegral = Integral;
        end
    end
    
    % Update previous value for the next iteration
    previousValue = currentValue;
    

end



% Close the serial port when done
fclose(s);
delete(s);
clear s;

% Save the data to a .mat file
save('/Users/koenkiewiet/Documents/MATLAB/KOEN_Proef2.mat', 'RPM_plotted', 'flow_plotted', 'pressure_plotted','time_values');
% Save the figure to a PDF file
% saveas(gcf, '/Users/koenkiewiet/Downloads/Proef1.1.pdf');

% Close the serial port when done
fclose(s);
delete(s);
clear s;
