a = 0.05;
G = 6.67 * 10^-11;
i = 60;
omega = -90;
M = 1;
P = sqrt(4 * pi^2 * a^3 / (G * M));
figure(1)
filename = 'radial_vel.gif';
for e = 0.1:0.1:0.9
    sum = 0;
    for theta = 1:1:720
        dist = a*(1-e^2)/(1 + e * cosd(theta));
        a_v = sqrt(G * M * a * (1 - e^2))/dist^2;
        d_t = 1 / a_v;
        sum = sum + d_t;
        sum1 = sum/(60*60);
        sum_t(theta) = sum1;
        v_r = (2 * pi * a * sind(i) * (e * cosd(omega) + cosd(omega + theta))) / (P * sqrt(1 - e^2));
        radial_vel(theta) = v_r;
    end 
    plot(sum_t,radial_vel)
    drawnow
    frame = getframe(1);
    im = frame2im(frame);
    [imind,cm] = rgb2ind(im,256);
    if e == 0.1;
        imwrite(imind,cm,filename,'gif', 'Loopcount',inf);
    else
        imwrite(imind,cm,filename,'gif','WriteMode','append');
    end
end


