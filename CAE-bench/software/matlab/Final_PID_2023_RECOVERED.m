% =========================================================================
% Final_PID.m  —  2023 closed-loop speed controller for the compressed-air
%                 Wankel bench.  Author: Niek Hilbrands, BaIP 2023-24.
%                 Handed on by Max Kloosterman, 23 January 2024.
%
% PROVENANCE AND WARNING
%   This file was RECOVERED as text through the Google Drive API from
%   drive.google.com/file/d/1AHEYelm9op-rKECdSCq290AfyVtu5YcN
%   The API returns a markdown-escaped rendering, which has been mechanically
%   un-escaped here.  It is byte-for-byte faithful in every line I could
%   verify, but it is NOT the original file.  Before relying on it, download
%   the original from the link above and diff the two.
%
% WHY THIS FILE MATTERS
%   1. It is the origin of the "negative Kp and Kd, positive Ki" baseline
%      quoted in the Energy-Based Speed Regulation manuscript.  See below.
%   2. Its speed calculation is EVENT-BASED and therefore CORRECT.  It times
%      one full revolution and computes 60/elapsed.  The 2024 Python rewrite
%      replaced this with a windowed pulse count that assumes a 1 s window
%      while the Arduino publishes every ~207 ms, which is the source of the
%      x4.84 speed error in all 2024 data.  See docs/06_KNOWN_ISSUES.md.
%   3. Its flow is labelled L/hour, which is correct.  The 2024 rewrite
%      labels the same quantity L/min.
%   4. The commanded angle is clamped to 0-45 degrees, which is the origin of
%      the "stalls near 40 to 50 degrees" statement in the manuscript.
%
% DEPENDENCIES
%   MATLAB with the Instrument Control Toolbox (serial/fopen/fscanf).
%   serial() is removed in newer MATLAB; use serialport() if this errors.
% =========================================================================

clc
clear

% Open the serial port (adjust the COM port and baud rate accordingly)
%s = serial('/dev/cu.usbmodem1101', 'BaudRate', 19200);
s = serial('COM4', 'BaudRate', 19200);

% Close any existing open connections on COM3
%openConnections = instrfind('Port', '/dev/cu.usbmodem1101', 'Status', 'open');
openConnections = instrfind('Port', 'COM4', 'Status', 'open');

if ~isempty(openConnections)
    fclose(openConnections);
end
fopen(s);

% PID constants                    <-- the manuscript's baseline gains
Kp = -0.003;
Ki =  0.0002;
Kd = -0.003;

desiredRPM = 1500;                 % Desired RPM
error = 0;

% Outliers parameters
window_size = 10;
outlier_threshold = 400;
outlier_pressure_threshold = 0.2;
outlier_flow_threshold = 300;

% Initialize variables
triggers = 0;
triggerAngle = 0;
previousValue = 0;
timeElapsed = 0;
Angle = 0;
RPM_values = [];
time_values = [];
error_values = [];
angle_values = [];
pressure_values = [];
triggerFirstRun = 0;
previousAvgError = 0;
previousIntegral = 0;

currentAVGRPMvec = [];
AvgError = 0;
output = 0;
Proportional = 0;
Integral = 0;
Derivative = 0;
data = [];

RPM_plotted = [];
flow_plotted = [];
pressure_plotted = [];
flow_values = [];

% Start measuring time
tic;

% Create the initial plot
figure;

subplot(2, 1, 1);
yyaxis left;
h1 = plot(0, 0);                    % Initial point
ylabel('RPM');
hold on;

% Add a green dotted line at y = DesiredRpm
yline(desiredRPM, 'g--', 'Desired RPM');

% Use right y-axis for Angle
yyaxis right;
h4 = plot(0, 0, 'Color', 'r');      % Initial point
ylabel('Angle (degrees)');

% Configure plot
xlabel('Time (s)');
title('Real-Time RPM and Angle Plot');
grid on;

% Flow plot
subplot(2, 1, 2);
yyaxis left;
h2 = plot(0, 0);                    % Create initial plot for Pressure
ylabel('Pressure (Bar)');
hold on;

% Pressure plot
yyaxis right;
h3 = plot(0, 0, 'Color', 'r');      % Create initial plot for Flow
ylabel('Flow (L/Hour)');

xlabel('Time (s)');
title('Real-Time Flow and Pressure');
grid on;

% Main loop for real-time plotting
while true
    drawnow;

    % Read the trigger value from Arduino
    rawValue = fscanf(s, '%d,%f,%f');
    rawValue = [rawValue; timeElapsed];
    data = [data; rawValue'];
    rawValue = data(end,1);

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
            flow = sum(data(flownumbers,3))/elapsedTime;
            flow_rate = (flow/11) * 60;          % flowrate L/hour

            flow_values = [flow_values, flow_rate];

            if length(flow_values) > window_size
                flow_filtered = movmean(flow_values(end-window_size+1:end), window_size);
            else
                flow_filtered = flow_rate;       % Setting first run to zero
            end
            outliers = abs(flow_values(end) - flow_filtered(end)) > outlier_flow_threshold;
            flow_values(end) = flow_filtered(end);

            pressure = data(end,2);
            pressure_values = [pressure_values, pressure];

            % Filtering pressure values
            if length(pressure_values) > window_size
                pressure_filtered = movmean(pressure_values(end-window_size+1:end), window_size);
            else
                pressure_filtered = pressure;    % Setting first run to zero
            end

            % Identify and replace outliers
            outliers = abs(pressure_values(end) - pressure_filtered(end)) > outlier_pressure_threshold;
            pressure_values(end) = pressure_filtered(end);

            % Filtering RPM values
            if length(RPM_values) > window_size
                RPM_filtered = movmean(RPM_values(end-window_size+1:end), window_size);
            else
                RPM_filtered = RPM;              % Setting first run to zero
            end

            % Identify and replace outliers
            outliers = abs(RPM_values(end) - RPM_filtered(end)) > outlier_threshold;
            RPM_values(end) = RPM_filtered(end);

            error = desiredRPM - RPM_values(end);
            error_values = [error_values, error];

            Rotations = window_size;             % Actual rotations times three
            RotationsPropellor = Rotations * 1;

            % Calculating the angle every 10 rotations
            if triggerAngle == RotationsPropellor
                if triggerFirstRun == RotationsPropellor

                    output = 0;
                    Integral = 0;

                else
                    AvgError = sum(error_values((end-Rotations+1):end))/Rotations;

                    for i = length(error_values)-Rotations+1:length(error_values)
                        posVec = length(error_values)-Rotations+1:length(error_values);

                        if abs(error_values(i)) > 1.25 * mean(error_values((length(RPM_values)-Rotations+1):length(error_values)))
                            posVec(find(posVec == i)) = [];   % remove outlier
                            currentAVGRPM = mean(error_values(posVec));
                        elseif abs(error_values(i)) < 0.75 * mean(error_values((length(error_values)-Rotations+1):length(error_values)))
                            posVec(find(posVec == i)) = [];   % remove outlier
                            currentAVGRPM = mean(error_values(posVec));
                        else
                            currentAVGRPM = mean(error_values(posVec));
                        end
                    end
                    currentAVGRPMvec = [currentAVGRPMvec, currentAVGRPM];
                    usedAVG_Error = error_values(posVec(end));

                    Proportional = Kp * usedAVG_Error;
                    Integral = previousIntegral+(usedAVG_Error*(time_values(end)-time_values(end-Rotations+1)));
                    Derivative = Kd * ((usedAVG_Error-previousAvgError)/(time_values(end)-time_values(end-Rotations+1)));
                    output = Proportional + Ki * Integral + Derivative;

                    previousAvgError = usedAVG_Error;

                end

                previousIntegral = Integral;

                Angle = Angle + output;
                Angle = round(max(0, min(45, Angle)));   % Ensure angle is between 0 and 45 degrees

                triggerAngle = 0;                        % Reset for the next full rotation
                fprintf(s, '2%d', Angle);
            end

            % Update the angle values array
            angle_values = [angle_values, Angle];

            % Update cumulative time values array
            timeElapsed = timeElapsed + elapsedTime;
            time_values = [time_values, timeElapsed];

            % Reset variables for the next full rotation
            triggers = 0;

            RPM_plotted = RPM_values;
            RPM_plotted(1:window_size) = 0;

            flow_plotted = flow_values;

            pressure_plotted = pressure_values;

            yyaxis right;
            set(h4, 'XData', time_values, 'YData', angle_values);
            ylabel('Angle (degrees)');
            yyaxis left;                         % Switch back to left y-axis for RPM
            set(h1, 'XData', time_values, 'YData', RPM_plotted);   % Update RPM plot

            yyaxis right;
            set(h3, 'XData', time_values, 'YData', flow_plotted);  % Update Flow plot
            ylabel('Flow (L/Hour)');
            yyaxis left;                         % Switch back to left y-axis for RPM
            set(h2, 'XData', time_values, 'YData', pressure_plotted); % Update Pressure plot

            tic;                                 % Start measuring time again

        end
    end

    % Update previous value for the next iteration
    previousValue = currentValue;

end

% Close the serial port when done
fclose(s);
delete(s);
clear s;
