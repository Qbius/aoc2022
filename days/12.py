def parse(lines):
    grid = [list(line) for line in lines]
    start = next((x, y) for x in range(len(grid[0])) for y in range(len(grid)) if grid[y][x] == 'S')
    end = next((x, y) for x in range(len(grid[0])) for y in range(len(grid)) if grid[y][x] == 'E')
    return start, end, [list(line.replace('S', 'a').replace('E', 'z')) for line in lines]

def djikstra(start, endpoints, grid):
    width = len(grid[0])
    height = len(grid)
    max_distance = width * height
    distances = {(x, y): max_distance for x in range(width) for y in range(height)}
    distances[start] = 0
    visited = set()
    not_visited = lambda point: point not in visited
    while any(map(not_visited, endpoints)):
        current = min(filter(not_visited, distances), key=distances.get)
        cx, cy = current

        in_bounds = lambda x, y: x >= 0 and x < width and y >= 0 and y < height
        ok_label = lambda x, y: (ord(grid[cy][cx]) - ord(grid[y][x])) <= 1
        
        nbrs = [(cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)]
        nbrs = [point for point in nbrs if not_visited(point) and in_bounds(*point) and ok_label(*point)]

        for point in nbrs:
            distances[point] = distances[current] + 1
        visited.add(current)
    return min(map(distances.get, endpoints))

def first(start, end, grid):
    return djikstra(end, [start], grid)

def second(_start, end, grid):
    ass = [(x, y) for x in range(len(grid[0])) for y in range(len(grid)) if grid[y][x] == 'a']
    return djikstra(end, ass, grid)

example = '''Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi'''