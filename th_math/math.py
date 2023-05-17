import math
from scipy.optimize import curve_fit
import numpy as np
import itertools # Dosimeter combinations for trilateration
from scipy.stats import norm # Gaussian distribution

from scipy.stats import multivariate_normal # Gaussian multivariate distribution
# import random

# import pandas as pd

from scipy.optimize import curve_fit


def sq(val):
  return val**2


# TODO: figure out if these are needed. Meybe they were for exp fitting to get the values that i now have fixed?
    # generated data for plotting
    # def GenerateExpData(a, b, x_min, x_max, steps):
    #   step = (x_max - x_min) / steps

    #   xs = np.zeros(steps)
    #   ys = np.zeros(steps)
    #   i = 0
    #   while ((x_min + step * i) < x_max):
    #     xs[i] = x_min + step * i
    #     ys[i] = FittedExponent(xs[i], a, b)
    #     i += 1

    #   return xs, ys


    # # distance to radiation
    # def FittedExponent(x, a, b):
    #   y = a * np.exp(b * x)

    #   return y

    # # radiation to distance
    # def FittedLogarithm(y, a, b):
    #   x = np.log(y/a) / b

    #   return x



# ------------------------
#  Dosimeter combinatorics
# ------------------------
# Was this included in the bacheclor thesis? I don't think so


# zero_divisions_count = 0
# def ExhaustiveTrilateration(ds):
#   tl_results = np.array([])
#   global zero_divisions_count

#   combinations = list(itertools.combinations(ds, 5))
#   for combo in combinations:
#     try:
#       rez = Trilateration3D(combo)
#       tl_results = np.append(tl_results, rez)
#     except ZeroDivisionError:
#       zero_divisions_count += 1
      
#   return tl_results

# def ExhaustiveSimplifiedTrilateration(ds):
#   tl_results = []
#   global zero_divisions_count

#   combinations = list(itertools.combinations(ds, 3))
#   for combo in combinations:
#     try:
#       rez = TrilaterationSimplified(combo, 3, 3)
#       tl_results.append(rez)
#     except ZeroDivisionError:
#       None
      
#   return np.array(tl_results)

# def NonExhaustiveTrilateration(ds):
#   tl_results = []
#   ds_count = len(ds)

#   for i in range(ds_count):
#     if (ds_count - i >= ds_min):
#       rez = TrilaterationWithDistance3D(ds[i : i + ds_min])
#     else:
#       temp1 = ds[ : ds_min - (ds_count - i)]
#       temp2 = ds[i : ]
#       rez = TrilaterationWithDistance3D([*(temp1), *(temp2)])
#     tl_results.append(rez)

#   return np.array(tl_results)

