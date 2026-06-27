import sys
import heapq

sys.setrecursionlimit(10000)


def volume(heightmap):
    if not heightmap or len(heightmap) == 1 and len(heightmap[0]) == 1:
        return 0

    rows = len(heightmap)
    cols = len(heightmap[0])
    
    # Create a priority queue to process cells in increasing order of height
    heap = []
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    
    # Add all border cells to the priority queue
    for i in range(rows):
        for j in [0, cols - 1]:
            heapq.heappush(heap, (heightmap[i][j], i, j))
            visited[i][j] = True
    
    for j in range(cols):
        for i in [0, rows - 1]:
            if not visited[i][j]:
                heapq.heappush(heap, (heightmap[i][j], i, j))
                visited[i][j] = True
    
    # Directions for moving to adjacent cells (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    total_volume = 0
    
    while heap:
        current_height, i, j = heapq.heappop(heap)
        
        for di, dj in directions:
            ni, nj = i + di, j + dj
            
            # Check if the neighbor is within bounds and not visited
            if 0 <= ni < rows and 0 <= nj < cols and not visited[ni][nj]:
                # The water level for the neighbor is the maximum between the current height and the neighbor's height
                new_height = max(current_height, heightmap[ni][nj])
                
                # If the neighbor's height is less than the new height, it can hold water
                if heightmap[ni][nj] < new_height:
                    total_volume += new_height - heightmap[ni][nj]
                    heightmap[ni][nj] = new_height  # Update the heightmap to the water level
                
                # Mark the neighbor as visited and add it to the priority queue
                visited[ni][nj] = True
                heapq.heappush(heap, (new_height, ni, nj))
    
    return total_volume


# Test cases
hmap1 = [[8, 8, 8, 8, 6, 6, 6, 6],
         [8, 0, 0, 8, 6, 0, 0, 6],
         [8, 0, 0, 8, 6, 0, 0, 6],
         [8, 8, 8, 8, 6, 6, 6, 0]]

print("Test case 1:")
print("Heightmap:")
for line in hmap1:
    print(line)
result = volume([row[:] for row in hmap1])
print(f"Volume: {result}")  # Expected: 56

# Additional test cases
hmap2 = [[3, 3, 3, 3, 3],
         [3, 0, 0, 0, 3],
         [3, 3, 3, 0, 3],
         [3, 0, 0, 0, 3],
         [3, 0, 3, 3, 3],
         [3, 0, 0, 0, 3],
         [3, 3, 3, 0, 3]]

print("\nTest case 2:")
print("Heightmap:")
for line in hmap2:
    print(line)
result = volume([row[:] for row in hmap2])
print(f"Volume: {result}")  # Expected: 18

# Edge case: single cell
hmap3 = [[5]]
print("\nTest case 3 (single cell):")
print("Heightmap:")
for line in hmap3:
    print(line)
result = volume([row[:] for row in hmap3])
print(f"Volume: {result}")  # Expected: 0

# Edge case: all same height
hmap4 = [[1, 1, 1],
         [1, 1, 1],
         [1, 1, 1]]
print("\nTest case 4 (all same height):")
print("Heightmap:")
for line in hmap4:
    print(line)
result = volume([row[:] for row in hmap4])
print(f"Volume: {result}")  # Expected: 0

# Test case with negative heights
hmap5 = [[3, 3, 3, 3, 3],
         [3, 0, 0, 0, 3],
         [3, 3, 3, 0, 3],
         [3, 0, -2, 0, 3],
         [3, 0, 3, 3, 3],
         [3, 0, 0, 0, 3],
         [3, 3, 3, 1, -3]]

print("\nTest case 5 (with negative heights):")
print("Heightmap:")
for line in hmap5:
    print(line)
result = volume([row[:] for row in hmap5])
print(f"Volume: {result}")

# Test case from Codewars example
hmap6 = [[9, 9, 9, 9, 9],
         [9, 0, 1, 2, 9],
         [9, 7, 8, 3, 9],
         [9, 6, 5, 4, 9],
         [9, 9, 9, 9, 9]]

print("\nTest case 6 (Codewars example):")
print("Heightmap:")
for line in hmap6:
    print(line)
result = volume([row[:] for row in hmap6])
print(f"Volume: {result}")  # Expected: 15
