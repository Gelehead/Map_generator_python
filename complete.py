class Tile :
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.z = 0
    
class Map :
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.perlin_map = self.perlin()
        self.tiles = [[Tile(x, y) for x in range(length)] for y in range(width)]
        
    # most parameters have to be changed here for simplicity's sake
    def perlin(self, octaves=4, ):
        """
        @args : octaves
        @returns : length * width of perlin noise with 
        """
    
# see README for complete explanation of parameters 
def main() :
    LENGTH = 200
    WIDTH = 200
    