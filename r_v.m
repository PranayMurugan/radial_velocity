theta = [1:1:720];
i = 60;
P = 5;
a = 0.05;
e = 0;
g = [];

%for k = 0:30:90
    for j = 1:1:720
        t = theta(j) + omega
        r = (2 * pi * a * sin(i) * (cos(t) + e * cos(omega)))/(P * sqrt(1 - e^2));
        g(j) = r;
    end
    hold on;
    plot(g)
%end
hold off;