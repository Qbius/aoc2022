def parse(rawinpt):
    grid = [list(line) for line in rawinpt.split('\n')]
    start = next((x, y) for x in range(len(grid[0])) for y in range(len(grid)) if grid[y][x] == 'S')
    end = next((x, y) for x in range(len(grid[0])) for y in range(len(grid)) if grid[y][x] == 'E')
    return start, end, [list(line) for line in rawinpt.replace('S', 'a').replace('E', 'z').split('\n')]

def first(start, end, grid):
    width = len(grid[0])
    height = len(grid)
    max_distance = width * height
    distances = {(x, y): max_distance for x in range(width) for y in range(height)}
    distances[start] = 0
    visited = set()
    while end not in visited:
        current = min([point for point in distances.keys() if point not in visited], key=distances.get)
        cx, cy = current

        not_visited = lambda x, y: (x, y) not in visited
        in_bounds = lambda x, y: x >= 0 and x < width and y >= 0 and y < height
        ok_label = lambda x, y: (ord(grid[y][x]) - ord(grid[cy][cx])) in [0, 1]
        
        nbrs = [(cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)]
        nbrs = [point for point in nbrs if not_visited(*point) and in_bounds(*point) and ok_label(*point)]

        for point in nbrs:
            distances[point] = distances[current] + 1
        visited.add(current)
    return distances[end]

def second(start, end, grid):
    pass

example = '''Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi'''