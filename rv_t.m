%theta = [0:1:720];
e = 0.9;
a = 0.05;
G = 6.67 * 10^-11;
i = 60;
sum = 0;
omega = -90;
m_p = 0.000002988;
M = 1;
P = sqrt(4 * pi^2 * a^3 / (G * M))
for theta = 1:1:720
    dist = a*(1-e^2)/(1 + e * cosd(theta));
    a_v = sqrt(G * M * a * (1 - e^2))/dist^2;
    d_t = 1 / a_v;
    sum = sum + d_t;
    sum_t(theta) = sum;
    v_r = (2 * pi * a * sind(i) * (e * cosd(omega) + cosd(omega + theta))) / (P * sqrt(1 - e^2));
    radial_vel(theta) = v_r;
end 
plot(sum_t,radial_vel)
