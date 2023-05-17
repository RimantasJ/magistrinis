from th_math.math import *
from global_variables import *
import scipy as sc
from scipy.stats import norm

# @jit(nopython=True)
def mixture_density_maximum_1d(xs):
  x_axis = np.linspace(-1, 10, 1000)
  mdf = 0
  len_xs = len(xs)

  # NOTE im using SCALE_GLOBAL, that is declared somewhere globaly
  for x in xs:
    pdf = norm.pdf(x_axis, x, SCALE_GLOBAL)
    mdf += (pdf / len_xs)
    # mdf += pdf # Alt

  return x_axis[np.argmax(mdf)]

def mixture_density_maximum_1d_alt(xs):
  x_axis = np.linspace(-1, 10, 1000)
  mdf = 0
  len_xs = len(xs)

  # NOTE im using SCALE_GLOBAL, that is declared somewhere globaly
  for x in xs:
    pdf = norm.pdf(x_axis, x, SCALE_GLOBAL)
    # mdf += (pdf / len_xs)
    mdf += pdf # Alt

  return x_axis[np.argmax(mdf)]

def mixture_density_maximum_3d(tl_results):
  calc_points = tl_results.T
  mix_max_3d = np.zeros(3)
  mix_max_3d[0] = mixture_density_maximum_1d(calc_points[0])
  mix_max_3d[1] = mixture_density_maximum_1d(calc_points[1])
  mix_max_3d[2] = mixture_density_maximum_1d(calc_points[2])

  return mix_max_3d

# @jit
def MixtureDensityMaximum1DAlt(xs):
  x_axis = np.linspace(-1, 10, 1000)
  scale = 0.06667
  mdf = 0
  len_xs = len(xs)

  # NOTE im using SCALE_GLOBAL, that is declared somewhere globaly
  for x in xs:
    pdf = norm.pdf(x_axis, x, SCALE_GLOBAL)
    mdf += pdf

  return x_axis[np.argmax(mdf)]

def MixtureDensityMaximum3DAlt(tl_results):
  calc_points = tl_results.T
  mix_max_3d = np.zeros(3)
  mix_max_3d[0] = MixtureDensityMaximum1DAlt(calc_points[0])
  mix_max_3d[1] = MixtureDensityMaximum1DAlt(calc_points[1])
  mix_max_3d[2] = mixture_density_maximum_1d(calc_points[2])

  return mix_max_3d