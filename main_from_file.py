from plotter import Plotter
import csv

class RCA:
    def __init__(self, boundaries):
        self.boundaries = boundaries
    def get_intersect_times(self, x, y):
        cnt = 0
        ori_x, ori_y = x, y
        for b in self.boundaries:
            # reset the node to the original position
            x = ori_x
            y = ori_y
            if (x == b.sx and y == b.sy) or (x == b.ex and y == b.ey): # the node is a vertex of the boundary
                return -1 
            if (y == b.sy and y == b.ey and min(b.sx, b.ex) <= x <= max(b.sx, b.ex)): # the node is on the harizonal boundary
                return -1
            if x == b.sx and x == b.ex and b.sy <= y <= b.ey: # the node is on the harizonal boundary
                return -1
            if (y == b.sy or y == b.ey): 
                if b.sy != b.ey: 
                    y += 1e-6
                else:
                    continue
            if y > b.ey or y < b.sy:
                continue
            if x >= max(b.sx, b.ex):
                continue
            if x < min(b.sx, b.ex):
                cnt += 1
                continue
            if b.ex == b.sx: # avoid zero-divide
                slope_b = 1e9
            else:
                slope_b = (b.ey - b.sy) / (b.ex - b.sx)
            if x == b.sx:
                slope_p = 1e9
            else:
                slope_p = (y - b.sy) / (x - b.sx) 
            if slope_p > slope_b:
                cnt += 1
            elif slope_p < slope_b:
                continue
            else:
                return -1 # boundary
        return cnt
    
class Edge:
    def __init__(self, start, end):
        if start[1] < end[1]:
            self.sx = start[0]
            self.sy = start[1]
            self.ex = end[0]
            self.ey = end[1]
        else:
            self.sx = end[0]
            self.sy = end[1]
            self.ex = start[0]
            self.ey = start[1]


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
                boundaries.append(Edge(a, b))
            r = [int(i) for i in r]
            x.append(r[1])
            y.append(r[2])
            max_x = max(max_x, r[1])
            min_x = min(min_x, r[1])
            max_y = max(max_y, r[2])
            min_y = min(min_y, r[2])
        plotter.add_polygon(x, y)
    print('read input.csv')
    test_point_cor = []
    with open('./input.csv', 'r') as inp:
        f = csv.reader(inp)
        headers = next(f)
        for r in f:
            r = [float(i) for i in r]
            test_point_cor.append((r[1], r[2]))

    print('categorize points')
    rca = RCA(boundaries)
    category = []
    for p in test_point_cor:
        if p[0] < min_x or p[0] > max_x or p[1] < min_y or p[1] > max_y:
            plotter.add_point(p[0], p[1], 'outside')
            category.append('outside')
        else:
            t = rca.get_intersect_times(p[0], p[1])
            # t = rca.get_intersect_times(2, 0)
            if t == -1:
                plotter.add_point(p[0], p[1], 'boundary')
                category.append('boundary')
            elif t % 2:
                plotter.add_point(p[0], p[1], 'inside')
                category.append('inside')
            else:
                plotter.add_point(p[0], p[1], 'outside')
                category.append('outside')

    print('write output.csv')
    with open('output.csv', 'wt') as f:
        output = csv.writer(f)
        output.writerow(['id', 'category'])
        for i, c in enumerate(category):
            output.writerow([i+1, c])
    
    print('plot polygon and points')
    plotter.show()


if __name__ == '__main__':
    main()
