# Simple Python Map Generator

The code will be divided into 2 files > `generator.py` for the minimalist version and `complete.py` for the complete version

It will be good to note that `generator.py` is sufficient for a maximum ( or close to maximum ) grade

The other version is purely for the ego and a mockup version of what another project should look like.

## Minimalist version

It should be noted that the map, again, for simplicity sake will only be a glorified 2d UV map ( could be re generated based on a greyscale noise 2d map )

### intended code structure 

1. Multi octaves perlin noise generation
    - smooth using fade perlin function WHEN GENERATING the point
    - smooth THE WHOLE MAP after generating
2. Generate SCAD code 
    - coloring function based on height

### code commentary 

Partial commentary will already be on the code itself but some choice will be here

#### General
 - no class will be needed as we only need a 2d int array 

#### export_to_scad
 - was hell tweaking this, scad is cool but harsh sometimes
 - `normalized height` depends on the maximum and minimum value of the map, it helps after that scaling it to emphasize heights and get the color index
 - `color_idx` corresponds to the index of the colors list matching the height
 - blocks that should go negative instead just have a size of 1 
 - `module_terrain_block` not gonna lie, this one is on IA, i hard forced classic block creating and could not get it right for the life of me
 - `x_scale` and `y_scale` are greater than 1 to not have gaps in the map

#### PerlinOctave
 - `feature_size` should be $\frac{sampling_rate}{frequency}$ but we assume that we want every pixel to count so it usually is 1
 - we decrease the importance of each newly generated perlin noise before adding it to the final result to have more details in the map
 - after generating the map, we normalize by the total amplitude to have smoother terrain features 
    - note : interesting to look at without it, try commenting the code
 - after doing `res[y][x] /= totalAmplitude` ( to normalize the resulting height ), we compress each height dependent on wheter or not it is positive
    - The numbers here are quite sensitive, avoid touching as the result might be awful when baddly tuned

#### Perlin
 - `grid width = frequency` and `grid length = frequency` can be modified to have non uniform feature distribution
 - `grid_cell` is the corresponding cell in the gradient grid
 - `pos` is the position of the point WITHIN the cell grid (between 0 and 1)
 - `pab` is the gradient of a corner of a cell
    - 00 for upper-left
    - 01 for upper-right
    - 10 for lower-left
    - 11 for lower right
 - `vab` is the dot product between the gradient and the distance vector
 - `f` is the smoothed position using fade function
 - `top` and `bottom` are the components for smooth bilinear interpolation

#### Main
 - `flat values` serves to get `min_val` and `max_val` which helps normalize and enhance the values afterward
 - After getting the result and before exporting it, we enhance heights because, without that, the terrain would be REALLY dull, try it yourself
 - export the terrain


## Complete version

### intended code structure ( by dificulty )

1. Generate multiple octaves of perlin noise on a 2D map
2. Apply smoothing function
3. Add details 
    1. vegetation
        1. Trees
        2. bushes
        3. coral
    2. volcanos
    3. rivers
    4. erosion
        1. rivers
        2. valleys
    5. Human structures 
    6. Caves

cant be bothered with hexagonal tiles

## WORK IN PROGRESS 