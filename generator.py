import random
import numpy as np

# Every code commentary necessary to understand the program is in the
# README.md, PLEASEEEE go read it

## Utility functions
def dot(v0, v1):
    return (v0[0] * v1[0]) + (v0[1] * v1[1])

def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)

def lerp(a, b, t):
    return a + t * (b - a)

def export_to_scad(filename, noise_grid, colors, scale=1.0, height_scale=10.0, vertical_exaggeration=2.5):
    length = len(noise_grid[0])
    width = len(noise_grid)
    
    flat_grid = [val for row in noise_grid for val in row]
    min_val = min(flat_grid)
    max_val = max(flat_grid)
    range_val = max_val - min_val
    
    with open(filename, "w") as f:
        f.write("// Generated terrain using Perlin noise\n")
        f.write("// Using blocks with enhanced height scaling\n\n")
        
        # Create a module for a single terrain block with varying x, y scale
        f.write("module terrain_block(x, y, z, h, c, x_scale=1, y_scale=1) {\n")
        f.write("    color(c)\n")
        f.write("        translate([x, y, z])\n")
        f.write("        cube([x_scale, y_scale, h]);\n")
        f.write("}\n\n")
        
        f.write("module terrain() {\n")
        
        for y in range(width):
            for x in range(length):
                height = noise_grid[y][x]
                normalized_height = (height - min_val) / range_val
                
                color_idx = min(int(normalized_height * len(colors)), len(colors) - 1)
                r, g, b = colors[color_idx]
                
                height = height * height_scale
                if height > 0:
                    height = height * (1 + normalized_height * (vertical_exaggeration - 1))
                
                if height >= 0:
                    f.write(f"    terrain_block({x * scale}, {y * scale}, 0, {height:.2f} + 1, [{r/255}, {g/255}, {b/255}], {scale:.2f}, {scale:.2f});\n")
                else:
                    f.write(f"    terrain_block({x * scale}, {y * scale}, 0, 1, [{r/255}, {g/255}, {b/255}], {scale:.2f}, {scale:.2f});\n")
        
        f.write("}\n\n")
        
        f.write("terrain();\n")

## -------------------- main program --------------------

def perlinOctave(length, width, octaves, frequency, persistence, sampling_rate=1):
    def generateGradients(grid_width, grid_length):
        gradient_grid = [[[0, 0] for _ in range(grid_length)] for _ in range(grid_width)]
        for y in range(grid_width):
            for x in range(grid_length):
                angle = random.uniform(0, 2 * 3.14159)
                gradient_grid[y][x] = [np.cos(angle), np.sin(angle)]
        return gradient_grid
                 
    def perlin(feature_size):
        grid_width = int(width / feature_size + 1)
        grid_length = int(length / feature_size + 1)
        
        gradients = generateGradients(grid_width, grid_length)
        
        noise_grid = [[0 for x in range(width)] for y in range(length)]
        
        for y in range(length):
            for x in range(width):
                grid_cell = [int(x/feature_size), int(y/feature_size)]
                
                pos = [(x % feature_size) / feature_size, (y % feature_size) / feature_size]
                
                if grid_cell[1] + 1 >= grid_width or grid_cell[0] + 1 >= grid_length:
                    continue
                
                p00 = gradients[grid_cell[1]][grid_cell[0]]
                p10 = gradients[grid_cell[1]][grid_cell[0] + 1]
                p01 = gradients[grid_cell[1] + 1][grid_cell[0]]
                p11 = gradients[grid_cell[1] + 1][grid_cell[0] + 1]
                
                v00 = dot(p00, [pos[0], pos[1]])
                v10 = dot(p10, [pos[0] - 1, pos[1]])
                v01 = dot(p01, [pos[0], pos[1] - 1])
                v11 = dot(p11, [pos[0] - 1, pos[1] - 1])
                
                f = list(map(fade, pos))
                
                top = lerp(v00, v10, f[0])
                bottom = lerp(v01, v11, f[0])
                value = lerp(top, bottom, f[1])
                
                noise_grid[y][x] = value
        
        return noise_grid
    
    ## ------------ main function ------------
    
    res = [[0 for _ in range(width)] for _ in range(length)]
    
    amplitude = 1
    totalAmplitude = 0
    
    base_feature_size = (sampling_rate / frequency) * length
    
    for o in range(octaves):
        feature_size = base_feature_size / (2 ** o)
        feature_size = 1 if feature_size < 1 else feature_size
        
        octave_noise = perlin(feature_size)
        for y in range(length):
            for x in range(width):
                if y < len(octave_noise) and x < len(octave_noise[0]):
                    res[y][x] += octave_noise[y][x] * amplitude
        
        totalAmplitude += amplitude
        amplitude *= persistence
    
    for y in range(length):
        for x in range(width):
            res[y][x] /= totalAmplitude
            
            if res[y][x] > 0:
                res[y][x] = res[y][x] ** 0.8
            else:
                res[y][x] = -((-res[y][x]) ** 0.9)
    
    return res, totalAmplitude


def main():
    LENGTH = 80
    WIDTH = 80
    OCTAVES = 8
    FREQUENCY = 3
    PERSISTENCE = 0.3
    SAMPLING_RATE = 1
    
    colors = [
        (0, 0, 128),      # Deep water (deep blue)
        (0, 0, 255),      # Water (blue)
        (0, 128, 255),    # Shallow water (light blue)
        (240, 240, 64),   # Sand (yellow)
        (32, 160, 0),     # Grass (green)
        (32, 120, 0),     # Forest (darker green)
        (160, 160, 0),    # Hills (yellow-green)
        (128, 128, 128),  # Mountain (gray)
        (200, 200, 200),  # Higher mountains (light gray)
        (255, 255, 255)   # Snow peaks (white)
    ]
    
    noise_grid, _ = perlinOctave(
        LENGTH, 
        WIDTH, 
        OCTAVES, 
        FREQUENCY, 
        PERSISTENCE,
        SAMPLING_RATE
    )
    
    flat_values = [val for row in noise_grid for val in row]
    min_val = min(flat_values)
    max_val = max(flat_values)
    
    for y in range(LENGTH):
        for x in range(WIDTH):
            normalized = 2 * (noise_grid[y][x] - min_val) / (max_val - min_val) - 1
            
            if normalized > 0:
                enhanced = normalized ** 1.55
            else:
                enhanced = -(-normalized) ** 1.2 
                
            noise_grid[y][x] = enhanced
    
    export_to_scad(
        "terrain.scad", 
        noise_grid, 
        colors, 
        scale=1.0, 
        height_scale=15.0, 
        vertical_exaggeration=4.0
    )

if __name__ == "__main__":
    main()