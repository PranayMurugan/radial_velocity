theta = [0:1:720];
i = 60;
P = 5;
a = 0.05;
e = 0;
g = [];

for k = 0:30:90
    for j = 0:1:720
        t = theta(j+1) + k;
        r = (2 * pi * a * sind(i) * (cosd(t) + e * cosd(k)))/(P * sqrt(1 - e^2));
        g(j+1) = r;
    end
    hold on;
    plot(theta,g)
end
hold off;
