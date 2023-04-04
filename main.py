import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# range in which tigers are going to be drawn
min_range = 0
max_range = 100

min_side_length = 5
max_side_length = 20

num_of_points = 20

x_tigers = []
y_tigers = []

tigers = []

x_triangle = []
y_triangle = []


class Tiger:
    def __init__(self):
        self.x = np.random.randint(min_range, max_range)
        self.y = np.random.randint(min_range, max_range)
        self.a = np.random.randint(min_side_length, max_side_length)
        self.b = np.random.randint(min_side_length, max_side_length)
        self.rot = np.random.randint(0, 360)


for i in range(num_of_points):

    x_points = []
    y_points = []
    tiger = Tiger()

    # checking if the triangle exists
    if tiger.b * 2 <= tiger.a:
        while tiger.b * 2 <= tiger.a:
            tiger = Tiger()

    # calculations to determine where vertices of the triangle are
    h = np.sqrt(pow(tiger.b, 2) - pow(tiger.a, 2) / 4)
    h2 = np.sqrt((pow(h, 2) / 9) + (pow(tiger.a, 2) / 4))

    # np. beta - radians, betaD - degrees
    beta = np.arccos((- pow(tiger.a, 2) + pow(h2, 2) + pow(h2, 2)) / (2 * h2 * h2))
    betaD = (beta * 180) / np.pi
    gammaD = (360 - betaD) / 2
    gamma = np.radians(gammaD)

    # angle of rotation of the triangle
    angle = np.radians(tiger.rot)

    # calculating coordinates of the vertices
    p1x = tiger.x + h2 * np.cos(angle)
    p1y = tiger.y + h2 * np.sin(angle)

    p2x = tiger.x + h2 * np.cos(angle + beta)
    p2y = tiger.y + h2 * np.sin(angle + beta)

    p3x = tiger.x + (2 * (h / 3)) * np.cos(angle + beta + gamma)
    p3y = tiger.y + (2 * (h / 3)) * np.sin(angle + beta + gamma)

    x_tigers.append(tiger.x)
    y_tigers.append(tiger.y)

    x_points.append(p1x)
    y_points.append(p1y)
    x_points.append(p2x)
    y_points.append(p2y)
    x_points.append(p3x)
    y_points.append(p3y)
    x_points.append(p1x)
    y_points.append(p1y)
    x_triangle.append(x_points)
    y_triangle.append(y_points)

    for j in range(0, 3):
        tigers.append([x_points[j], y_points[j], 0])

# choosing first point to have something to compare against when looking for the point of the smallest y coordinate
smallest = tigers[0][1]

# looking for the point of the smallest y coordinate
for i in range(len(tigers)):
    if tigers[i][1] < smallest:
        smallest = tigers[i][1]

convexhull = []
P1 = smallest

for i in range(len(tigers)):
    if tigers[i][1] == smallest:
        P1 = tigers[i]
        convexhull.append(P1)

angles = []
points = []

angles2 = []
points2 = []

biggest = -1
biggest2 = -1

# jarvis algorithm
for i in range(len(tigers)):
    if i == 0:
        for j in range(len(tigers)):
            P0P1 = np.sqrt(pow(P1[0] - (P1[0] - 2), 2))
            P2 = tigers[j]
            P1P2 = np.sqrt(pow(P2[0] - P1[0], 2) + pow(P2[1] - P1[1], 2))
            P0P2 = np.sqrt(pow((P1[0] - 2) - P2[0], 2) + pow(P1[1] - P2[1], 2))
            if 2 * P1P2 * P0P1 == 0:
                angle = -2
            else:
                cosAlfa = (- pow(P0P2, 2) + pow(P1P2, 2) + pow(P0P1, 2)) / (2 * P1P2 * P0P1)
                angle = np.arccos(cosAlfa)
            angles.append(angle)
            points.append(P2)
            if angle > biggest:
                biggest = angle

        for k in range(len(tigers)):
            if angles[k] == biggest:
                next_point = points[k]
                convexhull.append(next_point)

    else:
        for q in range(1, len(tigers)):
            if convexhull[-1] == convexhull[0]:
                break
            P00 = convexhull[q - 1]
            P11 = convexhull[q]
            for n in range(len(tigers)):
                P22 = tigers[n]
                P0P12 = np.sqrt(pow(P11[0] - P00[0], 2) + pow(P11[1] - P00[1], 2))
                P1P22 = np.sqrt(pow(P22[0] - P11[0], 2) + pow(P22[1] - P11[1], 2))
                P0P22 = np.sqrt(pow(P00[0] - P22[0], 2) + pow(P00[1] - P22[1], 2))
                if 2 * P1P22 * P0P12 == 0:
                    angle2 = -2
                else:
                    cosAlfa2 = (-pow(P0P22, 2) + pow(P1P22, 2) + pow(P0P12, 2)) / (2 * P1P22 * P0P12)
                    angle2 = np.arccos(cosAlfa2)
                angles2.append(angle2)
                points2.append(P22)
                if angle2 > biggest2:
                    biggest2 = angle2

            for m in range(len(tigers)):
                if angles2[m] == biggest2:
                    convexhull.append(points2[m])

            biggest2 = -1
            points2.clear()
            angles2.clear()

length = len(convexhull)

fig, ax = plt.subplots()
plt.xlim(-20, 120)
plt.ylim(-20, 120)

for i in range(len(y_triangle)):
    triangles, = plt.plot(x_triangle[i], y_triangle[i], color='#FF8000')
    pts, = plt.plot(x_tigers[i], y_tigers[i], '.', color='black')

hull_x = []
hull_y = []

convex, = plt.plot([], [], linewidth=1.5, color='#8B4726')


def animate(u):
    hull_x.append(convexhull[u][0])
    hull_y.append(convexhull[u][1])
    convex.set_data(hull_x, hull_y)

    return convex


animated = animation.FuncAnimation(fig, animate, frames=length, interval=300, repeat=False)

plt.show()
