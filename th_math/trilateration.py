from th_math.math import *
from global_variables import *
# Calculates three coordinates, uses absolute distances
def trilateration_3d_abs (ds):
    x1, y1, z1, r1 = ds[0].x,      ds[0].y,      ds[0].z,      ds[0].distance ** 2
    x2, y2, z2, r2 = ds[1].x - x1, ds[1].y - y1, ds[1].z - z1, ds[1].distance ** 2
    x3, y3, z3, r3 = ds[2].x - x1, ds[2].y - y1, ds[2].z - z1, ds[2].distance ** 2
    x4, y4, z4, r4 = ds[3].x - x1, ds[3].y - y1, ds[3].z - z1, ds[3].distance ** 2

    r21 = r2 - r1
    r31 = r3 - r1
    r41 = r4 - r1

    t2 = sq(x2) + sq(y2) + sq(z2)
    t3 = sq(x3) + sq(y3) + sq(z3)
    t4 = sq(x4) + sq(y4) + sq(z4)

    xu1 = z2*(r41 - t4) + z4*(t2 - r21)
    xu2 = y2*z3 - y3*z2
    xu3 = z2*(r31 - t3) + z3*(t2 - r21)
    xu4 = y2*z4 - y4*z2
    xu = xu1 * xu2 - xu3 * xu4
    xl1 = (x2 * z4 - x4 * z2) * (y2 * z3 - y3 * z2)
    xl2 = (x2 * z3 - x3 * z2) * (y2 * z4 - y4 * z2)
    xl = 2 * (xl1 - xl2)
    x = xu / xl
    
    if (math.isinf(x) or math.isnan(x)):
        raise ZeroDivisionError

    yu1 = z2 * (r31 - t3)
    yu2 = z3 * (t2 - r21)
    yu3 = 2 * x * (x2 * z3 - x3 * z2)
    yu = yu1 + yu2 - yu3
    yl = 2 * (y2 * z3 - y3 * z2)
    y = yu / yl

    z = (t2 - r21 - 2 * x * x2 - 2 * y * y2) / (2 * z2)

    return [(x+x1), (y+y1), (z+z1)]

# Calculates three coordinates, uses proportional distances
def trilateration_3d_rel (ds):
    x1, y1, z1, r1 = ds[0].x,      ds[0].y,      ds[0].z,      ds[0].distance ** 2
    x2, y2, z2, r2 = ds[1].x - x1, ds[1].y - y1, ds[1].z - z1, ds[1].distance ** 2
    x3, y3, z3, r3 = ds[2].x - x1, ds[2].y - y1, ds[2].z - z1, ds[2].distance ** 2
    x4, y4, z4, r4 = ds[3].x - x1, ds[3].y - y1, ds[3].z - z1, ds[3].distance ** 2
    x5, y5, z5, r5 = ds[4].x - x1, ds[4].y - y1, ds[4].z - z1, ds[4].distance ** 2

    r21 = r2 - r1
    r31 = r3 - r1
    r41 = r4 - r1
    r51 = r5 - r1

    x23 = x2 * r31 - x3 * r21
    x24 = x2 * r41 - x4 * r21
    x25 = x2 * r51 - x5 * r21
    y23 = y2 * r31 - y3 * r21
    y24 = y2 * r41 - y4 * r21
    y25 = y2 * r51 - y5 * r21
    z23 = z2 * r31 - z3 * r21
    z24 = z2 * r41 - z4 * r21
    z25 = z2 * r51 - z5 * r21

    t2 = sq(x2) + sq(y2) + sq(z2)
    t3 = sq(x3) + sq(y3) + sq(z3)
    t4 = sq(x4) + sq(y4) + sq(z4)
    t5 = sq(x5) + sq(y5) + sq(z5)

    xu1 = z23 * (t4 * r21 - t2 * r41) - z24 * (t3 * r21 - t2 * r31)
    xu2 = y25 * z23 - y23 * z25
    xu3 = z23 * (t5 * r21 - t2 * r51) - z25 * (t3 * r21 - t2 * r31)
    xu4 = y24 * z23 - y23 * z24
    xu = xu1 * xu2 - xu3 * xu4
    xl1 = (x25 * z23 - x23 * z25) * (y24 * z23 - y23 * z24)
    xl2 = (x24 * z23 - x23 * z24) * (y25 * z23 - y23 * z25)
    xl = 2 * (xl1 - xl2)
    x = xu / xl
    if (math.isinf(x) or math.isnan(x)):
        raise ZeroDivisionError

    yu1 = z24 * (t3 * r21 - t2 * r31)
    yu2 = z23 * (t4 * r21 - t2 * r41)
    yu3 = 2 * x * (x24 * z23 - x23 * z24)
    yu = yu1 - yu2 - yu3
    yl = 2 * (y24 * z23 - y23 * z24)
    y = yu / yl

    z = (t2 * r31 - t3 * r21 - 2 * x * x23 - 2 * y * y23) / (2 * z23)

    return [(x+x1), (y+y1), (z+z1)]

def trilateration_1d_abs (ds, src_x, src_y):
    x1, y1, z1, r1 = ds[0].x,      ds[0].y,      ds[0].z,      ds[0].distance ** 2
    x2, y2, z2, r2 = ds[1].x - x1, ds[1].y - y1, ds[1].z - z1, ds[1].distance ** 2
    x, y = (src_x - x1), (src_y - y1)

    r21 = r2 - r1
    t2 = sq(x2) + sq(y2) + sq(z2)

    zu = t2 - r21 - 2 * x2 * x - 2 * y2 * y
    zl = 2 * z2
    z = zu / zl
    if (math.isinf(z) or math.isnan(z)):
        raise ZeroDivisionError

    return z+z1

# Calculates one coordinate, uses proportional distances
def trilateration_1d_rel (ds, src_x, src_y):
    x1, y1, z1, r1 = ds[0].x,      ds[0].y,      ds[0].z,      ds[0].distance ** 2
    x2, y2, z2, r2 = ds[1].x - x1, ds[1].y - y1, ds[1].z - z1, ds[1].distance ** 2
    x3, y3, z3, r3 = ds[2].x - x1, ds[2].y - y1, ds[2].z - z1, ds[2].distance ** 2
    x, y = (src_x - x1), (src_y - y1)

    r21 = r2 - r1
    r31 = r3 - r1

    zu1 = (sq(x2) - 2 * x2 * x + sq(y2) - 2 * y2 * y + sq(z2)) * r31
    zu2 = (sq(x3) - 2 * x3 * x + sq(y3) - 2 * y3 * y + sq(z3)) * r21
    zl = 2 * (z2 * r31 - z3 * r21)
    z = (zu1 - zu2) / zl
    if (math.isinf(z) or math.isnan(z)):
        raise ZeroDivisionError

    return z+z1


