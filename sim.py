#reference from this article
# "https://medium.com/analytics-vidhya/simulating-the-solar-system-with-under-100-lines-of-python-code-5c53b3039fc6"

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from astropy.time import Time
from astroquery.jplhorizons import Horizons

sim_start_date = "2021-08-21"
sim_duration = 5*365
# m_earth = 

class Object:
    def __init__(self, name, rad, color, r, v):
        self.name = name
        self.r = np.array(r, dtype= np.float)
        self.v = np.array(v, dtype = np.float)
        self.xs = []
        self.ys = []
        self.plot = ax.scatter(r[0], r[1], color = color, s = rad**2, edgecolor=None,zorder=10)
        self.line, = ax.plot([],[], color = color, linewidth = 1.4)

class SolarSystem:
    def __init__(self, sun):
        self.sun = sun
        self.planets = []
        self.time = None
        self.timestamp = ax.text(.03, .94, 'Date: ', color='w',transform=ax.transAxes, fontsize=20)
    def add_planet(self, planet):
        self.planets.append(planet)
    def evolve(self):
        dt = 1.0
        self.time+=dt
        plots = []
        lines = []
        for p in self.planets:
            p.r += p.v*dt
            acc = -2.959e-4 * p.r / np.sum(p.r**2)**(3./2)
            p.v+=acc*dt
            p.xs.append(p.r[0])
            p.ys.append(p.r[1])
            p.plot.set_offsets(p.r[:2])
            p.line.set_xdata(p.xs)
            p.line.set_ydata(p.ys)
            plots.append(p.plot)
            lines.append(p.line)
        self.timestamp.set_text('Date: ' + Time(self.time, format='jd').iso)
        return plots+lines+[self.timestamp]

img = plt.imread('bg2.jpg')
# plt.style.use('dark_background')
fig = plt.figure(figsize=[6,6])

ax=plt.axes([0.,0.,1.,1.], xlim=(-4.0, 4.0), ylim=(-2.0, 2.0))
ax.set_aspect('equal')
ax.axis('off')
ax.imshow(img, extent = [-4, 4, -2, 2])
# , extent=[0, 400, 0, 300])
ss = SolarSystem(Object("Sun", 28, 'red', [0,0,0],[0,0,0]))
ss.time = Time(sim_start_date).jd
colors = ['grey','orange', 'blue', 'chocolate']
sizes = [0.38, 0.95, 1.0, 0.53]
names = ['Mercury', 'Venus', 'Earth', 'Mars']
orbrad = [0.47, 0.73, 1, 1.5]

for i, nasaid in enumerate([199,299,399,499]):
    obj = Horizons(id=nasaid, location="@sun", epochs=ss.time, id_type='id').vectors()
    ss.add_planet(Object(nasaid, 20*sizes[i], colors[i], [np.double(obj[xi]) for xi in ['x','y','z']], [np.double(obj[vxi]) for vxi in ['vx','vy','vz']]))
    ax.text(0, -(orbrad[i]+0.1), names[i], color=colors[i], zorder=1000, ha='center', fontsize='small')

def animate(i):
    return ss.evolve()

ani = animation.FuncAnimation(fig, animate, repeat = False, frames = sim_duration, blit = True, interval = 20)

plt.show()

# ani.save('solar_system_6in_150dpi.mp4', fps=60, dpi=150)

# python sim.py
