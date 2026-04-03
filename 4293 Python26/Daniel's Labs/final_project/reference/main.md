clear; clc;

% ---------------- baseMVA ----------------
baseMVA = 100;

% ---------------- bus data ----------------
% Columns:
%  1 bus_i  2 type  3 Pd  4 Qd  5 Gs  6 Bs  7 area  8 Vm  9 Va 10 baseKV 11 zone 12 Vmax 13 Vmin

% Column 2 type = 3, slack bus
% Column 2 type = 2, PV bus
% Column 2 type = 1, PQ bus


bus = [
    1   3   0     0     0     0   1   1.04    0       345  1  1.1  0.9;
    2   2   0     0     0     0   1   1.025   0       345  1  1.1  0.9;
    3   2   0     0     0     0   1   1.025   0       345  1  1.1  0.9;
    4   1  125    50    0     0   1   1.0     0       345  1  1.1  0.9;
    5   1   90    30    0     0   1   1.0     0       345  1  1.1  0.9;
    6   1   0     0     0     0   1   1.0     0       345  1  1.1  0.9;
    7   1  100    35    0     0   1   1.0     0       345  1  1.1  0.9;
    8   1   0     0     0     0   1   1.0     0       345  1  1.1  0.9;
    9   1  125    50    0     0   1   1.0     0       345  1  1.1  0.9;
];


%Increase real loads by 5% on all PQ buses (only Pd)
    % bus4 = 125*1.05 = 131.25
    % bus5 = 90*1.05  = 94.5
    % bus6 = 0*1.05   = 0
    % bus7 = 100*1.05 = 105
    % bus8 = 0*1.05   = 0
    % bus9 = 125*1.05 = 131.25
    

    %---------------- bus with 5% increase ----------------
%{
 bus = [
    1   3   0       0     0     0   1   1.04    0       345  1  1.1  0.9;
    2   2   0       0     0     0   1   1.025   0       345  1  1.1  0.9;
    3   2   0       0     0     0   1   1.025   0       345  1  1.1  0.9;
    4   1   131.25  50    0     0   1   1.0     0       345  1  1.1  0.9;
    5   1   94.5    30    0     0   1   1.0     0       345  1  1.1  0.9;
    6   1   0       0     0     0   1   1.0     0       345  1  1.1  0.9;
    7   1   105     35    0     0   1   1.0     0       345  1  1.1  0.9;
    8   1   0       0     0     0   1   1.0     0       345  1  1.1  0.9;
    9   1   131.25  50    0     0   1   1.0     0       345  1  1.1  0.9;
];
%}

% ---------------- generator data ----------------
% Columns:
%  1 bus  2 Pg  3 Qg  4 Qmax  5 Qmin  6 Vg  7 mBase  8 status ...
gen = [
    1   71.64   27.05   999  -999  1.04   100  1;
    2   163.0   6.79    999  -999  1.025  100  1;
    3    85.0  -10.92   999  -999  1.025  100  1;
];

% ---------------- branch data ----------------
% Columns:
%  1 fbus  2 tbus  3 r  4 x  5 b  6 rateA  7 rateB  8 rateC ...
branch = [
    1   4   0.0000   0.0576   0.0000   250  250  250;
    4   5   0.0170   0.0920   0.1580   250  250  250;
    5   6   0.0390   0.1700   0.3580   150  150  150;
    3   6   0.0000   0.0586   0.0000   300  300  300;
    6   7   0.0119   0.1008   0.2090   150  150  150;
    7   8   0.0085   0.0720   0.1490   250  250  250;
    8   2   0.0000   0.0625   0.0000   250  250  250;
    8   9   0.0320   0.1610   0.3060   250  250  250;
    9   4   0.0100   0.0850   0.1760   250  250  250;
];

% ---------------- run NR power flow ----------------
out = pf_dubon(bus, branch, gen, baseMVA, 1e-8, 30, 0.7); %% Students need to work inside this pf_XX function (completed)

% ---------------- display results ----------------
disp('      Bus     Vm(pu)    Va(deg)')
disp([ (1:length(out.Vm))' out.Vm out.Va ])
fprintf('Slack: P=%.3f MW, Q=%.3f MVAr\n', out.slackP_MW, out.slackQ_MVAr)
fprintf('Total loss = %.3f MW\n', out.Ploss_total_MW)
disp('    From      To       Pij       Qij       Pji       Qji      Ploss(MW)')
disp(out.branch_flow)


