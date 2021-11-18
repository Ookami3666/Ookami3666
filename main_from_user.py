from plotter import Plotter
from main_from_file import RCA, Edge
import csv

def main():
    plotter = Plotter()
    print('read polygon.csv')
    max_x, max_y = 0, 0
    min_x, min_y = 0, 0
    x, y = [], []
    boundaries = []
    with open('./polygon.csv', 'r') as poly:
        f = csv.reader(poly)
        headers = next(f)
        f = list(f)
        for i, r in enumerate(f):
            if i+1 < len(f):
                a = [float(i) for i in f[i][1:]]
                b = [float(i) for i in f[i+1][1:]]
                boundaries.append(Edge(a, b)) # create boundaries
            r = [int(i) for i in r]
            x.append(r[1])
            y.append(r[2])
            max_x = max(max_x, r[1])
            min_x = min(min_x, r[1])
            max_y = max(max_y, r[2])
            min_y = min(min_y, r[2])
        plotter.add_polygon(x, y)

    print('Insert point information')
    x = float(input('x coordinate: '))
    y = float(input('y coordinate: '))

    print('categorize point')
    rca = RCA(boundaries)
    category = []
    p = (x, y) 
    if p[0] < min_x or p[0] > max_x or p[1] < min_y or p[1] > max_y:
        plotter.add_point(p[0], p[1], 'outside')
        category.append('outside')
    else:
        t = rca.get_intersect_times(p[0], p[1])
        if t == -1:
            plotter.add_point(p[0], p[1], 'boundary')
            category.append('boundary')
        elif t % 2:
            plotter.add_point(p[0], p[1], 'inside')
            category.append('inside')
        else:
            plotter.add_point(p[0], p[1], 'outside')
            category.append('outside')

    print('plot polygon and point')
    plotter.show()


if __name__ == '__main__':
    main()
