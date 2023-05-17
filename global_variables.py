import numpy as np

class Dosimeter3D:
    x: float
    y: float
    z: float
    radiation: float
    distance: float
    
    
    def __init__ (self, x=None, y=None, z=None, r=None, d=None):
        self.x = x
        self.y = y
        self.z = z
        self.radiation = r
        self.distance = d
        
    # def _get_distance(self):
    #     return self.distance
    
    # def _set_distance(self, d):
    #     if not isinstance(d, float):
    #         raise TypeError("Distance but be of type float")
    #     self.distance = d
        
    # distance = property(_get_distance, _set_distance)

    def print(self):
        print(self.x, ' ', self.y, ' ', self.z, ' : ', "%.2f" % self.radiation, ' : ', "%.2f" % self.distance)

# Already Calculated dosimeter exponent koeficients
dosimeter_exp_ab = [
    [ 0.16801284, -0.37641622],
    [ 2.23576675, -1.13339008],
    [ 2.41308608, -1.45751485],
    [ 1.54596901, -0.92266818],
    [ 1.73770635, -1.01474088],
    [ 2.06235769, -1.19327526],
    [ 1.75301363, -1.03443367],
    [ 1.81073478, -1.07940669],
    [ 0.14224586, -0.37226811]
  ]

# dosimeter positions
ds = np.array([
    Dosimeter3D(x=1, y=5, z=2),
    Dosimeter3D(x=1, y=5, z=5),
    Dosimeter3D(x=1, y=5, z=8),
    Dosimeter3D(x=5, y=4, z=2),
    Dosimeter3D(x=5, y=4, z=5),
    Dosimeter3D(x=5, y=4, z=8),
    Dosimeter3D(x=2, y=1, z=2),
    Dosimeter3D(x=2, y=1, z=5),
    Dosimeter3D(x=2, y=1, z=8)] )

# global const settings
# Mixture density parameter
SCALE_GLOBAL=1

# Parameters needed to mark what were the real values to be used for comparison
START_COORDINATE = 0
TIMER_START_OFFSET = -500
STEP_TIME = 5150
STEP_SIZE = 0.5
STEP_CUTOFF_MARGIN = 200 # ms to cutoff
IS_GOING_DOWN = False

# using previously calculated log values via fitting
DS_AB_PRECALC = [
        [ 0.16801284, -0.37641622],
        [ 2.23576675, -1.13339008],
        [ 2.41308608, -1.45751485],
        [ 1.54596901, -0.92266818],
        [ 1.73770635, -1.01474088],
        [ 2.06235769, -1.19327526],
        [ 1.75301363, -1.03443367],
        [ 1.81073478, -1.07940669],
        [ 0.14224586, -0.37226811]
    ]