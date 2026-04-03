function out = pf_dubon(bus, branch, gen, baseMVA, tol, maxIter, damp)

% ---------------- defaults & indices ----------------
if nargin < 5 || isempty(tol),     tol     = 1e-6; end
if nargin < 6 || isempty(maxIter), maxIter = 20;   end
if nargin < 7 || isempty(damp),    damp    = 1.0;  end
BUS_I = 1; TYPE = 2; PD = 3; QD = 4; GS = 5; BS = 6; VM = 8; VA = 9;
F_BUS = 1; T_BUS = 2; BR_R = 3; BR_X = 4; BR_B = 5;
GEN_BUS = 1; PG = 2; QG = 3;

bus    = double(bus); 
branch = double(branch);
gen    = double(gen);

% ---------------- quick sanity checks ----------------
if any(~isfinite([bus(:); branch(:); gen(:)]))
    error('nr_pf:NaNInf','Input contains NaN/Inf in bus/branch/gen.');
end
if ~any(bus(:,TYPE)==3)
    error('nr_pf:NoSlack','No slack bus (TYPE==3) found.');
end
if sum(bus(:,TYPE)==3) > 1
    warning('nr_pf:MultiSlack','More than one slack bus found; this can make J singular.');
end

nb = size(bus,1); % Place 1 Students work on (completed)
nl = size(branch,1); % Place 2 Students work on (completed)

% ---------------- ext->int bus index mapping ----------------
ext_id = bus(:,BUS_I);              
f_ext = branch(:,F_BUS);
t_ext = branch(:,T_BUS);

[ok_f, f] = ismember(f_ext, ext_id);
[ok_t, t] = ismember(t_ext, ext_id);
if ~all(ok_f) || ~all(ok_t)
    error('nr_pf:BranchRef','Some branch F/T bus IDs not found in BUS_I.');
end

[ok_g, gen_bus_int] = ismember(gen(:,GEN_BUS), ext_id);
if ~all(ok_g)
    error('nr_pf:GenRef','Some generator BUS IDs not found in BUS_I.');
end

% ---------------- Ybus (pi line model) ----------------
r = branch(:,BR_R);   x = branch(:,BR_X);  b = branch(:,BR_B);
z = r + 1j*x;
bad = ~isfinite(z) | (abs(z) == 0);
if any(bad)
    warning('nr_pf:ZeroZ','Found invalid/zero z=r+jx; add tiny reactance to avoid 1/0.');
    z(bad) = 1j*1e-6;
end
y_series = 1 ./ z;          
y_shunt  = 1j * b / 2;      %
y_shunt(~isfinite(y_shunt)) = 0;   % 

Ybus = sparse(nb, nb);

for k = 1:nl
    i = f(k); j = t(k); y = y_series(k);
    Ybus(i,i) = Ybus(i,i) + y;
    Ybus(j,j) = Ybus(j,j) + y; 
    Ybus(i,j) = Ybus(i,j) - y; % Place 3 Students work on (completed)
    Ybus(j,i) = Ybus(j,i) - y; % Place 4 Students work on (completed)
end

for k = 1:nl
    i = f(k); j = t(k); ys = y_shunt(k);
    if ys ~= 0
        Ybus(i,i) = Ybus(i,i) + ys;
        Ybus(j,j) = Ybus(j,j) + ys;
    end
end
% Bus shunt (GS+jBS)/baseMVA
if size(bus,2) >= BS
    Ybus = Ybus + sparse(1:nb,1:nb, bus(:,GS)./baseMVA + 1j*bus(:,BS)./baseMVA, nb, nb);
end

% ---------------- Sbus (p.u.) ----------------
Pd = bus(:,PD);
Qd = bus(:,QD);
Pg = accumarray(gen_bus_int, gen(:,PG), [nb 1], @sum, 0);
Qg = accumarray(gen_bus_int, gen(:,QG), [nb 1], @sum, 0);
Sbus = (Pg - Pd)/baseMVA + 1j*(Qg - Qd)/baseMVA;

% ---------------- initial V ----------------
V  = bus(:,VM) .* exp(1j*deg2rad(bus(:,VA))); % Place 5 Students work on (completed)
type = bus(:,TYPE);
slk = find(type==3);
pv  = find(type==2);
pq  = find(type==1);

% ---------------- NR iterations ----------------
success = false;
for iter = 1:maxIter
    I = Ybus * V;  % Place 6 Students work on (completed)
    S = V .* conj(I); % Place 7 Students work on (completed)
    mis = Sbus - S;          % \Deta S
    dP = real(mis); % Place 8 Students work on (completed)
    dQ = imag(mis); % Place 9 Students work on (completed)
    F  = [dP([pv; pq]); dQ(pq)];   
    if ~all(isfinite(F))
        error('levens_pf:MisNaN','Power mismatch contains NaN/Inf.');
    end

    if norm(F, inf) < tol
        success = true;
        break;
    end

  
    Vm = abs(V); Va = angle(V); % Place 10 Students work on (completed)
    G = real(Ybus); B = imag(Ybus);

    H = zeros(nb); N = zeros(nb);
    M = zeros(nb); L = zeros(nb);

    for i = 1:nb

        H(i,i) = - (Vm(i)^2) * B(i,i);
        M(i,i) =   (Vm(i)^2) * G(i,i);
        for k = 1:nb
            if k == i, continue; end
            theta = Va(i) - Va(k);
            Gik = G(i,k); Bik = B(i,k);

            H(i,k) =  Vm(i)*Vm(k)*( Gik*sin(theta) - Bik*cos(theta) );   % dP_i/dVa_k % Place 11 Students work on (completed)
            N(i,k) =  Vm(i)*( Gik*cos(theta) + Bik*sin(theta) );  % dP_i/dVm_k % Place 12 Students work on (completed)
            M(i,k) =  Vm(i)*Vm(k)*( -Gik*cos(theta) - Bik*sin(theta) );  % dQ_i/dVa_k % Place 13 Students work on (completed)
            L(i,k) =  Vm(i)*( Gik*sin(theta) - Bik*cos(theta) );  % dQ_i/dVm_k % Place 14 Students work on(completed)

     
            H(i,i) = H(i,i) - Vm(i)*Vm(k)*( Gik*sin(theta) - Bik*cos(theta) ); % Place 15 Students work on [this is the last place students need to work on] (completed)
            M(i,i) = M(i,i) - Vm(i)*Vm(k)*( -Gik*cos(theta) - Bik*sin(theta) );
            N(i,i) = N(i,i) + Vm(k)*( Gik*cos(theta) + Bik*sin(theta) );
            L(i,i) = L(i,i) + Vm(k)*( Gik*sin(theta) - Bik*cos(theta) );
        end
    end

    idxVa = [pv; pq];
    idxVm = pq;
    J = [ H(idxVa, idxVa)   N(idxVa, idxVm) ;
          M(idxVm, idxVa)   L(idxVm, idxVm) ];

    if any(~isfinite(J(:)))
        error('nr_pf:JacNaN','Jacobian contains NaN/Inf, check input data (r/x/b/VM/VA/GS/BS).');
    end


    % LM: (J'*J + lambda*I) \ (J'*F)
    diagJ = diag(J);
    if isempty(diagJ), diagJ = 0; end
    lambda = 1e-8 * (norm(diagJ, 'inf')^2 + eps);
    A = J.'*J + lambda*eye(size(J,2));
    bvec = J.'*F;
    if any(~isfinite(A(:))) || any(~isfinite(bvec))
        error('nrpf:LMNaN','LM system contains NaN/Inf');
    end
    dx = A \ bvec;

    dVa = dx(1:length(idxVa));
    dVm = dx(length(idxVa)+1:end);

    if damp ~= 1.0
        dVa = damp * dVa;
        dVm = damp * dVm;
    end

    Va0 = angle(V);  Vm0 = abs(V);
    best_V = V; best_norm = norm(F, inf);
    step = 1.0;                      
    for ls = 1:8
        Va_try = Va0; Vm_try = Vm0;
        Va_try(idxVa) = Va0(idxVa) + step * dVa;
        Vm_try(idxVm) = Vm0(idxVm) + step * dVm;

        Vm_try(pv) = bus(pv, VM);

        V_try = Vm_try .* exp(1j*Va_try);

        V_try(slk) = bus(slk,VM) .* exp(1j*deg2rad(bus(slk,VA)));

        I_try = Ybus * V_try;
        S_try = V_try .* conj(I_try);
        mis_try = Sbus - S_try;
        F_try = [real(mis_try([pv; pq])); imag(mis_try(pq))];

        if ~all(isfinite(F_try)), step = step * 0.5; continue; end

        if norm(F_try, inf) < best_norm
            best_norm = norm(F_try, inf);
            best_V = V_try;
            break;
        else
            step = step * 0.5;
        end
    end

    V = best_V;
end

% ---------------- outputs ----------------
out.Vm = abs(V);
out.Va = rad2deg(angle(V));
out.Ybus = Ybus;


I = Ybus * V;
S = V .* conj(I);            % p.u.
out.P_inj = real(S) * baseMVA;   % MW
out.Q_inj = imag(S) * baseMVA;   % MVAr
S_slack   = S(slk) * baseMVA;
out.slackP_MW   = real(S_slack);
out.slackQ_MVAr = imag(S_slack);


branch_flow = zeros(nl, 7); % [from(to-extID) to-extID Pij Qij Pji Qji Ploss]
for k = 1:nl
    i = f(k); j = t(k);
    y_ser = 1 / (r(k) + 1j*x(k));
    b_half= 1j * b(k) / 2;

    
    if ~isfinite(y_ser), y_ser = 1/(1j*1e-6); end
    if ~isfinite(b_half), b_half = 0; end

    Iij = (V(i) - V(j)) * y_ser + V(i) * b_half;  % i->j
    Iji = (V(j) - V(i)) * y_ser + V(j) * b_half;  % j->i
    Sij = V(i) * conj(Iij);   % p.u.
    Sji = V(j) * conj(Iji);   % p.u.

    Pij = real(Sij) * baseMVA;  Qij = imag(Sij) * baseMVA;
    Pji = real(Sji) * baseMVA;  Qji = imag(Sji) * baseMVA;
    Ploss = Pij + Pji;          % MW


    branch_flow(k,:) = [f_ext(k), t_ext(k), Pij, Qij, Pji, Qji, Ploss];
end
out.branch_flow = branch_flow;
out.Ploss_total_MW = sum(branch_flow(:,7));
end
