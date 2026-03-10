#!/usr/bin/env python3
"""
GIF animation generator for GitHub Contribution Snake
"""

from PIL import Image, ImageDraw
from .config import SNAKE_CONFIG, COLORS

def generate_gif_animation(grid, snake_path, output_path, dark_mode=True):
    """Generate GIF animation of the snake eating contributions"""
    if not grid:
        print("No grid data available")
        return
        
    rows = len(grid[0])
    cols = len(grid)
    
    # Get configuration
    cell_size = SNAKE_CONFIG['cell_size']
    cell_spacing = SNAKE_CONFIG['cell_spacing']
    snake_length = SNAKE_CONFIG['snake_length']
    animation_duration = SNAKE_CONFIG['animation_duration']
    padding = SNAKE_CONFIG['padding']
    
    # Get colors based on theme
    colors = COLORS['dark'] if dark_mode else COLORS['light']
    
    # Calculate image dimensions with proper padding
    width = cols * (cell_size + cell_spacing) - cell_spacing + (padding * 2)
    height = rows * (cell_size + cell_spacing) - cell_spacing + (padding * 2)
    
    frames = []
    
    # Track which contributions have been eaten
    eaten_positions = set()
    
    print(f"Creating {len(snake_path) + snake_length} frames for GIF animation...")
    
    for frame_idx in range(len(snake_path) + snake_length):
        # Create frame
        img = Image.new('RGB', (width, height), colors['background'])
        draw = ImageDraw.Draw(img)
        
        # Mark positions that the snake head has visited as "eaten"
        if frame_idx < len(snake_path):
            snake_head_col, snake_head_row, _ = snake_path[frame_idx]
            eaten_positions.add((snake_head_col, snake_head_row))
        
        # Draw contribution grid
        for col in range(cols):
            for row in range(rows):
                if row >= len(grid[col]):
                    continue
                    
                x = col * (cell_size + cell_spacing) + padding
                y = row * (cell_size + cell_spacing) + padding
                
                # If this position has been eaten by the snake, show it as empty
                if (col, row) in eaten_positions:
                    level = 0  # Empty/eaten contribution
                else:
                    level = min(4, grid[col][row]['level'])
                
                color = colors['levels'][level]
                
                # Draw rounded rectangle
                draw.rounded_rectangle(
                    [x, y, x + cell_size, y + cell_size],
                    radius=2,
                    fill=color
                )
        
        # Draw snake
        for i in range(snake_length):
            snake_pos = frame_idx - i
            if 0 <= snake_pos < len(snake_path):
                col, row, contribution_count = snake_path[snake_pos]
                
                # Skip if out of bounds
                if col >= len(grid) or row >= len(grid[col]):
                    continue
                    
                x = col * (cell_size + cell_spacing) + padding
                y = row * (cell_size + cell_spacing) + padding
                
                # Snake head (brightest) with eating effect
                if i == 0:
                    color = colors['snake_head']
                    
                    # If eating a contribution, make the head glow/pulse
                    if contribution_count > 0:
                        # Eating effect - make head slightly larger and brighter
                        offset = 2
                        # Draw glow effect - different colors for light/dark theme
                        glow_color = '#ff9999' if dark_mode else '#ff6666'
                        draw.rounded_rectangle(
                            [x - offset - 1, y - offset - 1, x + cell_size + offset + 1, y + cell_size + offset + 1],
                            radius=4,
                            fill=glow_color
                        )
                        
                    # Draw the main head
                    offset = 1 if contribution_count > 0 else 0
                    draw.rounded_rectangle(
                        [x - offset, y - offset, x + cell_size + offset, y + cell_size + offset],
                        radius=3,
                        fill=color
                    )
                else:
                    # Snake body with fading effect
                    alpha = 1.0 - (i / snake_length) * 0.6
                    # Convert hex to RGB and apply alpha effect
                    snake_color = colors['snake']
                    if snake_color.startswith('#'):
                        rgb = tuple(int(snake_color[j:j+2], 16) for j in (1, 3, 5))
                        # Blend with background for fade effect
                        bg_rgb = tuple(int(colors['background'][j:j+2], 16) for j in (1, 3, 5))
                        blended = tuple(int(rgb[k] * alpha + bg_rgb[k] * (1 - alpha)) for k in range(3))
                        color = f"#{blended[0]:02x}{blended[1]:02x}{blended[2]:02x}"
                    else:
                        color = snake_color
                    
                    draw.rounded_rectangle(
                        [x, y, x + cell_size, y + cell_size],
                        radius=2,
                        fill=color
                    )
        
        frames.append(img)
    
    # Save GIF with optimized settings
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=animation_duration,
        loop=0,
        optimize=True
    )
    theme_name = "dark" if dark_mode else "light"
    print(f"GIF animation ({theme_name} theme) saved to: {output_path}")
