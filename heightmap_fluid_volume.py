import sys

sys.setrecursionlimit(10000)

class Point:
    def __init__(self, line: int, col: int, height: int):
        self.line = line
        self.col = col
        self.height = height
        self.bord = False
        self.visited = False
        self.max_height_obtained = False

    def __str__(self):
        return f"({self.line}, {self.col}, {self.height})"


class HeightMap:
    def __init__(self, hmap_: list):
        self.data = []
        self.volume_added = 0
        self.max_value = 100000000
        for i in range(len(hmap_)):
            self.data.append([])
            for j in range(len(hmap_[0])):
                self.data[i].append(Point(i, j, hmap_[i][j]))
        for points in self.data[0]:
            points.bord = True
        for points in self.data[-1]:
            points.bord = True
        for points in self.data:
            points[0].bord = True
            points[-1].bord = True
        self.nb_lines = len(self.data)
        self.nb_cols = len(self.data[0])

    def display(self):
        for points_line in self.data:
            l =[point_line.height for point_line in points_line]
            """print('[',end='')
            for h in l:
                print(f"{h}, ",end='')
            print(']')"""
            print(l)


    def get_bottom_point(self):
        point_min_height = None
        min_height = self.max_value
        for points in self.data:
            for point in points:
                if not point.bord and not point.max_height_obtained and point.height < min_height:
                    point_min_height = point
                    min_height = point.height
        return point_min_height

    def get_contiguous_list(self, point: Point, height:int, contiguous_list:list | None=None):
        if contiguous_list is None:
            contiguous_list = []
        if not point.bord and not point.visited and point.height == height:
            point.visited = True
            # print(f"({point.line}, {point.col}, {point.height})")
            # time.sleep(.5)
            contiguous_list.append(point)
            next_point = self.data[point.line+1][point.col]
            if not next_point.bord:
                self.get_contiguous_list(next_point, height, contiguous_list)
            next_point = self.data[point.line-1][point.col]
            if not next_point.bord:
                self.get_contiguous_list(next_point, height, contiguous_list)
            next_point = self.data[point.line][point.col+1]
            if not next_point.bord:
                self.get_contiguous_list(next_point, height, contiguous_list)
            next_point = self.data[point.line][point.col-1]
            if not next_point.bord:
                self.get_contiguous_list(next_point, height, contiguous_list)
        return contiguous_list

    def get_min_edge_of_a_point(self, point: Point)->():
        edge_height_list=set()
        if self.data[point.line+1][point.col].bord or self.data[point.line+1][point.col].height > point.height:
            edge_height_list.add((self.data[point.line+1][point.col].height, True if self.data[point.line+1][point.col].bord else False))
        if self.data[point.line-1][point.col].bord or self.data[point.line-1][point.col].height > point.height:
            edge_height_list.add((self.data[point.line-1][point.col].height, True if self.data[point.line-1][point.col].bord else False))
        if self.data[point.line][point.col+1].bord or self.data[point.line][point.col+1].height > point.height:
            edge_height_list.add((self.data[point.line][point.col+1].height, True if self.data[point.line][point.col+1].bord else False))
        if self.data[point.line][point.col-1].bord or self.data[point.line][point.col-1].height > point.height:
            edge_height_list.add((self.data[point.line][point.col-1].height, True if self.data[point.line][point.col-1].bord else False))
        if edge_height_list:
            min_edge = min(edge_height_list)
        else:
            min_edge = (point.height,False)
        # print("min_edge", min_edge)
        return min_edge

    def get_min_edge_of_a_contiguous_list(self, contiguous_list:list[Point])->int:
        min_edge,edge = self.get_min_edge_of_a_point(contiguous_list[0])
        for current_point in contiguous_list:
            current_min_edge,edge = self.get_min_edge_of_a_point(current_point)
            if (current_min_edge != current_point.height or edge)  and current_min_edge < min_edge:
                min_edge = current_min_edge
        # print('Contiguous list min_edge', min_edge)
        return min_edge


    def set_new_height_of_a_contiguous_list(self, new_height:int, contiguous_list:list[Point])->None:
        for point in contiguous_list:
            vol_added = max(0,new_height - point.height)
            self.volume_added += vol_added
            self.data[point.line][point.col].height = new_height
            self.data[point.line][point.col].visited = False



def volume(heightmap_):
    print('heightmap')
    for line in heightmap_:
        print(line)
    print('')
    if len(heightmap_) == 1 and len(heightmap_[0])==1:
        return 0
    heightmap = HeightMap(heightmap_)
    heightmap.display()


    actual_volume_added = heightmap.volume_added
    continue_loop = True
    while continue_loop:
        bottom_point = heightmap.get_bottom_point()
        print('Bottom point :',bottom_point)
        contiguous_points = heightmap.get_contiguous_list(bottom_point, bottom_point.height)
        print('Contiguous points of bottom point : ')
        for point in contiguous_points:
            print(point)
        new_height = heightmap.get_min_edge_of_a_contiguous_list(contiguous_points)
        # print('hauteur max',new_height)
        heightmap.set_new_height_of_a_contiguous_list(new_height, contiguous_points)
        heightmap.display()
        print('Volume added : ',heightmap.volume_added)
        if heightmap.volume_added != actual_volume_added:
            actual_volume_added = heightmap.volume_added
        else:
            for point in contiguous_points:
                heightmap.data[point.line][point.col].max_height_obtained= True
            if heightmap.get_bottom_point() is None:
                continue_loop = False
    heightmap.display()
    print('final volume added :',heightmap.volume_added)
    return heightmap.volume_added

# hmap = [[9, 9, 9, 9], [9, 1, 0, 9], [9, 0, 0, 9], [9, 9, 9, 9]]
hmap = [[8, 8, 8, 8, 6, 6, 6, 6],
                     [8, 0, 0, 8, 6, 0, 0, 6],
                     [8, 0, 0, 8, 6, 0, 0, 6],
                     [8, 8, 8, 8, 6, 6, 6, 0]]

hmap = [[3, 3, 3, 3, 3],
                     [3, 0, 0, 0, 3],
                     [3, 3, 3, 0, 3],
                     [3, 0, -2, 0, 3],
                     [3, 0, 3, 3, 3],
                     [3, 0, 0, 0, 3],
                     [3, 3, 3, 1, -3]]
hmap = [[1, 1, 1],
                     [1, 8, 1],
                     [1, 1, 1]]
hmap = [[9, 9, 9, 9, 9],
                     [9, 0, 1, 2, 9],
                     [9, 7, 8, 3, 9],
                     [9, 6, 5, 4, 9],
                     [9, 9, 9, 9, 9]]

hmap = [[3, 3, 3, 3, 3],
                     [3, 0, 0, 0, 3],
                     [3, 3, 3, 0, 3],
                     [3, 0, 0, 0, 3],
                     [3, 0, 3, 3, 3],
                     [3, 0, 0, 0, 3],
                     [3, 3, 3, 0, 3]]

hmap = [[2, 6, 14, 6, 0, -2, 6, 0, 1, 7],
[-3, 1, 13, 9, 4, -3, 13, 9, 12, 14],
[-2, 7, 7, 9, 1, 13, -1, -2, 12, -3],
[-2, 1, -5, 2, 13, 8, 11, 6, 8, 4],
[1, -2, 0, 7, 6, 11, -2, 1, -2, -2],
[12, 2, -3, -4, 5, 11, 3, -4, 5, 4],
[-3, 10, 3, 6, 4, 10, -5, -3, 0, 7],
[12, 4, 10, 6, 10, 3, -3, 7, 6, 1],
[5, 4, 14, -5, 9, 10, -5, 9, -1, -4],
[10, -5, 14, 0, 4, 3, 2, 7, -4, 2],
[8, -5, 14, 12, -2, 4, 14, 8, -1, -3],
[11, 5, 1, 3, 0, -1, -1, 4, 0, 14],
[6, 0, 8, 3, 6, 6, 11, 12, -5, -5],
[7, 14, 11, -3, 5, -1, 0, 2, 2, 11],
[9, 14, 9, -2, 11, 10, 3, 4, 0, -3]]

volume(hmap)
