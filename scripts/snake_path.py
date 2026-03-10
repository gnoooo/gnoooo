#!/usr/bin/env python3
"""
Snake path generation module
Creates intelligent paths for the snake to follow
"""

import random

def create_snake_path(grid):
    """Create a systematic path for the snake to follow through the entire contribution grid"""
    path = []
    if not grid:
        return path
        
    rows = len(grid[0]) if grid else 0
    cols = len(grid)
    
    # Create a priority list: contributions first, then empty spaces
    contributions = []
    empty_spaces = []
    
    for col in range(cols):
        for row in range(min(rows, len(grid[col]))):
            pos = (col, row, grid[col][row]['count'])
            if grid[col][row]['count'] > 0:
                contributions.append(pos)
            else:
                empty_spaces.append(pos)
    
    # Sort contributions by value (highest first)
    contributions.sort(key=lambda x: x[2], reverse=True)
    
    # Choose starting position - start from the beginning of the chart
    # GitHub contribution charts typically start from the first week (leftmost column)
    start_pos = None
    
    # Try to start from the leftmost column, preferably top-left (0,0)
    for col in range(min(3, cols)):  # Check first few columns
        for row in range(min(rows, len(grid[col]))):
            start_pos = (col, row, grid[col][row]['count'])
            break
        if start_pos:
            break
    
    # Fallback to (0,0) if nothing found
    if not start_pos:
        if cols > 0 and rows > 0:
            start_pos = (0, 0, grid[0][0]['count'] if len(grid[0]) > 0 else 0)
        else:
            start_pos = (0, 0, 0)
    
    visited = set()
    path.append(start_pos)
    visited.add((start_pos[0], start_pos[1]))
    
    def get_valid_moves(col, row):
        """Get valid adjacent moves (up, down, left, right only)"""
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # up, down, right, left
        
        for dc, dr in directions:
            new_col, new_row = col + dc, row + dr
            if (0 <= new_col < cols and 
                0 <= new_row < rows and 
                new_row < len(grid[new_col]) and
                (new_col, new_row) not in visited):
                moves.append((new_col, new_row, grid[new_col][new_row]['count']))
        return moves
    
    def move_towards_target(current_col, current_row, target_col, target_row):
        """Move one step toward target, return the move or None if blocked"""
        # Prefer horizontal movement first, then vertical
        if current_col != target_col:
            if current_col < target_col:
                next_col, next_row = current_col + 1, current_row
            else:
                next_col, next_row = current_col - 1, current_row
        elif current_row != target_row:
            if current_row < target_row:
                next_col, next_row = current_col, current_row + 1
            else:
                next_col, next_row = current_col, current_row - 1
        else:
            return None  # Already at target
        
        # Check if move is valid
        if (0 <= next_col < cols and 
            0 <= next_row < rows and 
            next_row < len(grid[next_col]) and
            (next_col, next_row) not in visited):
            return (next_col, next_row, grid[next_col][next_row]['count'])
        return None
    
    def find_path_to_nearest_unvisited():
        """Find path to nearest unvisited contribution or space"""
        current_col, current_row = path[-1][0], path[-1][1]
        
        # First, try to find unvisited contributions
        unvisited_contributions = [(col, row, count) for col, row, count in contributions 
                                 if (col, row) not in visited]
        
        # If no contributions left, find any unvisited space
        if not unvisited_contributions:
            unvisited_spaces = [(col, row, count) for col, row, count in empty_spaces 
                              if (col, row) not in visited]
            if unvisited_spaces:
                # Find nearest unvisited space
                distances = []
                for col, row, count in unvisited_spaces:
                    distance = abs(col - current_col) + abs(row - current_row)
                    distances.append((distance, col, row, count))
                distances.sort()
                if distances:
                    return distances[0][1], distances[0][2], distances[0][3]
            return None
        
        # Find nearest unvisited contribution
        distances = []
        for col, row, count in unvisited_contributions:
            distance = abs(col - current_col) + abs(row - current_row)
            distances.append((distance, col, row, count))
        
        distances.sort()
        return distances[0][1], distances[0][2], distances[0][3]
    
    # Main movement loop
    max_moves = cols * rows * 2  # Prevent infinite loops
    moves_made = 0
    stuck_count = 0
    
    while moves_made < max_moves:
        current_col, current_row = path[-1][0], path[-1][1]
        
        # Try to move toward nearest unvisited target
        target = find_path_to_nearest_unvisited()
        
        if target:
            target_col, target_row, target_count = target
            next_move = move_towards_target(current_col, current_row, target_col, target_row)
            
            if next_move:
                path.append(next_move)
                visited.add((next_move[0], next_move[1]))
                moves_made += 1
                stuck_count = 0
                continue
        
        # If can't move toward target, try any valid move
        valid_moves = get_valid_moves(current_col, current_row)
        
        if valid_moves:
            # Prefer moves with contributions
            contribution_moves = [move for move in valid_moves if move[2] > 0]
            if contribution_moves:
                next_move = random.choice(contribution_moves)
            else:
                next_move = random.choice(valid_moves)
            
            path.append(next_move)
            visited.add((next_move[0], next_move[1]))
            moves_made += 1
            stuck_count = 0
        else:
            # Snake is stuck, try to find any unvisited space we can reach
            stuck_count += 1
            if stuck_count > 5:
                break
            
            # Look for any unvisited position and try to "tunnel" there
            all_unvisited = []
            for col in range(cols):
                for row in range(min(rows, len(grid[col]))):
                    if (col, row) not in visited:
                        all_unvisited.append((col, row, grid[col][row]['count']))
            
            if not all_unvisited:
                break  # Everything visited
            
            # Pick a random unvisited position and try to get there
            target_col, target_row, target_count = random.choice(all_unvisited)
            
            # Try to make progress toward it
            next_move = move_towards_target(current_col, current_row, target_col, target_row)
            if next_move and (next_move[0], next_move[1]) not in visited:
                path.append(next_move)
                visited.add((next_move[0], next_move[1]))
                moves_made += 1
                stuck_count = 0
            else:
                # Really stuck, break out
                break
    
    # Add final sweeping motion to ensure we cover more of the grid
    remaining_unvisited = []
    for col in range(cols):
        for row in range(min(rows, len(grid[col]))):
            if (col, row) not in visited:
                remaining_unvisited.append((col, row, grid[col][row]['count']))
    
    # Try to visit remaining spaces with a simpler approach
    while remaining_unvisited and len(remaining_unvisited) > 0:
        current_col, current_row = path[-1][0], path[-1][1]
        
        # Find closest unvisited
        closest = min(remaining_unvisited, 
                     key=lambda x: abs(x[0] - current_col) + abs(x[1] - current_row))
        
        # Try to move one step toward it
        next_move = move_towards_target(current_col, current_row, closest[0], closest[1])
        
        if next_move and (next_move[0], next_move[1]) not in visited:
            path.append(next_move)
            visited.add((next_move[0], next_move[1]))
            remaining_unvisited = [(col, row, count) for col, row, count in remaining_unvisited 
                                 if (col, row) not in visited]
        else:
            break
    
    total_positions = sum(min(rows, len(grid[col])) for col in range(cols))
    coverage = len(visited) / total_positions * 100 if total_positions > 0 else 0
    contributions_found = sum(1 for _, _, count in path if count > 0)
    
    print(f"Snake path: {len(path)} moves, visited {len(visited)}/{total_positions} positions ({coverage:.1f}% coverage)")
    print(f"Found {contributions_found} contributions")
    
    return path
