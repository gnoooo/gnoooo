#!/usr/bin/env python3
"""
SVG animation generator for GitHub Contribution Snake
"""

import svgwrite
from .config import SNAKE_CONFIG, COLORS

def generate_svg_animation(grid, snake_path, output_path, dark_mode=False):
    """Generate SVG with snake path (simplified version)"""
    if not grid:
        print("No grid data available")
        return
        
    rows = len(grid[0])
    cols = len(grid)
    
    # Get configuration
    cell_size = SNAKE_CONFIG['cell_size']
    cell_spacing = SNAKE_CONFIG['cell_spacing']
    snake_length = SNAKE_CONFIG['snake_length']
    padding = 10
    
    # Calculate SVG dimensions with padding
    width = cols * (cell_size + cell_spacing) - cell_spacing + (padding * 2)
    height = rows * (cell_size + cell_spacing) - cell_spacing + (padding * 2)
    
    # Get colors for mode
    colors = COLORS['dark'] if dark_mode else COLORS['light']
    
    # Create SVG
    dwg = svgwrite.Drawing(output_path, size=(width, height))
    dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill=colors['background']))
    
    # Draw contribution grid
    for col in range(cols):
        for row in range(rows):
            x = col * (cell_size + cell_spacing) + padding
            y = row * (cell_size + cell_spacing) + padding
            
            if col < len(grid) and row < len(grid[col]):
                level = min(4, grid[col][row]['level'])
                color = colors['levels'][level]
            else:
                color = colors['levels'][0]
            
            rect = dwg.rect(
                insert=(x, y),
                size=(cell_size, cell_size),
                fill=color,
                rx=2
            )
            dwg.add(rect)
    
    # Draw snake at a specific position (25% through the path)
    snake_position = len(snake_path) // 4
    
    for i in range(snake_length):
        pos_idx = snake_position + i
        if pos_idx < len(snake_path):
            col, row, _ = snake_path[pos_idx]
            x = col * (cell_size + cell_spacing) + padding
            y = row * (cell_size + cell_spacing) + padding
            
            # Snake head (brightest) or body
            if i == 0:
                color = colors['snake_head']
                opacity = 1.0
            else:
                color = colors['snake']
                opacity = max(0.3, 1.0 - (i / snake_length) * 0.7)
            
            snake_rect = dwg.rect(
                insert=(x, y),
                size=(cell_size, cell_size),
                fill=color,
                fill_opacity=opacity,
                rx=2
            )
            dwg.add(snake_rect)
    
    dwg.save()
    print(f"SVG saved to: {output_path}")
