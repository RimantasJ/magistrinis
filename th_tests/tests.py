from th_math.math import *
from th_math.mixture_maximum import *
from th_math.trilateration import *
from th_math.distance_calculation import *
from th_formatting.formatting import *
from th_tests.tests import *

# TEST BASE
def RunLocalizationTest(ds, ds_data):
  min_ds = 5
  test_results = []

    # setting dosimeter radiation
  for i in range(len(ds_data[0])):

    for j in range(len(ds)):
        radiation = float(ds_data[j][i])
        if (radiation > 0.0032):
            ds[j].radiation = radiation
        else:
            ds[j].radiation = 0
    RadiationToDistanceNthRoot(ds, 2)
    no_zeros_ds = []
    for d in ds:
      if (d.radiation != 0):
        no_zeros_ds.append(d)

    # Calculating with exhaustinve trilateration
    tl_results = []
    combinations = list(itertools.combinations(no_zeros_ds, min_ds))
    for combo in combinations:
      try:
        tl_results.append(Trilateration3DProportionalDistances(combo))
      except ZeroDivisionError:
        None

    # Calculating highest density value
    if (len(tl_results) > 0):
      test_results.append(mixture_density_maximum_3d(np.array(tl_results)))
    else:
      test_results.append([0,0,0])

  return test_results

def RunTest(ds, file_path, time=5150):
  ds_data, timestamps = csv_to_array(txt_to_csv(file_path)) # opens file, returns structured dosimeter data
  z_values_dirty = MarkZValuesDirty(txt_to_csv(file_path), time, 8.5, 0)
  z_values_clean = MarkZValuesDeprecated(txt_to_csv(file_path), time, 8.5, 0)
  
  test_results = np.array(RunLocalizationTest(ds, ds_data))

  test_results_ts = np.column_stack((timestamps, z_values_dirty, z_values_clean, test_results.T[0],  test_results.T[1], test_results.T[2]))
  array_to_csv(file_path[9:-4] + '_sq', test_results_ts, ['time', 'real_z', 'clean_z', 'x', 'y', 'z'])

  return ('/content/' + file_path[9:-4] + '_sq.csv')


# TEST LOG BASE
def RunLocalizationTestLog(ds, ds_data):
  min_ds = 4
  test_results = []

  clear_radiation_noise(ds, ds_data)
  for i in range(len(ds_data[0])):
    # setting dosimeter radiation
    radiation_to_distance_log(ds)

    no_zeros_ds = []
    for d in ds:
      if (d.radiation != 0):
        no_zeros_ds.append(d)

    # Calculating with exhaustinve trilateration
    tl_results = []
    combinations = list(itertools.combinations(no_zeros_ds, min_ds))
    for combo in combinations:
      try:
        res = Trilateration3D(combo)
        tl_results.append(res)
      except ZeroDivisionError:
        None

    # Calculating highest density value
    if (len(tl_results) > 0):
      test_results.append(mixture_density_maximum_3d(np.array(tl_results)))
    else:
      test_results.append([0,0,0])

  return test_results

def RunTestLog(ds, file_path, time=5150):
  ds_data, timestamps = csv_to_array(txt_to_csv(file_path))
  z_values_dirty = MarkZValuesDirty(txt_to_csv(file_path), time, 8.5, 0)
  z_values_clean = MarkZValuesDeprecated(txt_to_csv(file_path), time, 8.5, 0)

  test_results = np.array(RunLocalizationTestLog(ds, ds_data))
  
  test_results_ts = np.column_stack((timestamps, z_values_dirty, z_values_clean, test_results.T[0],  test_results.T[1], test_results.T[2]))
  array_to_csv(file_path[9:-4] + '_log', test_results_ts, ['time', 'real_z', 'clean_z', 'x', 'y', 'z'])

  return ('/content/' + file_path[9:-4] + '_log.csv')

# TEST LOG PROPORTIONAL DISTANCES
def RunLocalizationTestLogProportionalDistances(ds, ds_data):
  min_ds = 5
  test_results = []

  for i in range(len(ds_data[0])):
    # setting dosimeter radiation
    for j in range(len(ds)):
      radiation = float(ds_data[j][i])
      if (radiation > 0.0032):
        ds[j].radiation = radiation
      else:
        ds[j].radiation = 0
    radiation_to_distance_log(ds)

    no_zeros_ds = []
    for d in ds:
      if (d.radiation != 0):
        no_zeros_ds.append(d)

    # Calculating with exhaustinve trilateration
    tl_results = []
    combinations = list(itertools.combinations(no_zeros_ds, min_ds))
    for combo in combinations:
      try:
        res = Trilateration3DProportionalDistances(combo)
        tl_results.append(res)
      except ZeroDivisionError:
        None

    # Calculating highest density value
    if (len(tl_results) > 0):
      test_results.append(mixture_density_maximum_3d(np.array(tl_results)))
    else:
      test_results.append([0,0,0])

  return test_results

def RunTestLogProportionalDistances(ds, file_path, time=5150):
  ds_data, timestamps = csv_to_array(txt_to_csv(file_path))
  z_values_dirty = MarkZValuesDirty(txt_to_csv(file_path), time, 8.5, 0)
  z_values_clean = MarkZValuesDeprecated(txt_to_csv(file_path), time, 8.5, 0)

  test_results = np.array(RunLocalizationTestLogProportionalDistances(ds, ds_data))
  
  test_results_ts = np.column_stack((timestamps, z_values_dirty, z_values_clean, test_results.T[0],  test_results.T[1], test_results.T[2]))
  array_to_csv(file_path[9:-4] + '_log_pd', test_results_ts, ['time', 'real_z', 'clean_z', 'x', 'y', 'z'])

  return ('/content/' + file_path[9:-4] + '_log_pd.csv')

# TEST SIMPLIFIED
def RunLocalizationTestSimplified(ds, ds_data, src_x=3, src_y=3):
  min_ds = 3
  test_results = []

  for i in range(len(ds_data[0])):
    # setting dosimeter radiation
    for j in range(len(ds)):
      radiation = float(ds_data[j][i])
      if (radiation > 0.0032):
        ds[j].radiation = radiation
      else:
        ds[j].radiation = 0
    RadiationToDistanceNthRoot(ds, 2)

    no_zeros_ds = []
    for d in ds:
      if (d.radiation != 0):
        no_zeros_ds.append(d)

    # Calculating with exhaustinve trilateration
    tl_results = []
    combinations = list(itertools.combinations(no_zeros_ds, min_ds))
    for combo in combinations:
      try:
        tl_results.append(Trilateration3DSimplified(combo, src_x, src_y))
      except ZeroDivisionError:
        None

    # Calculating highest density value
    if (len(tl_results) > 0):
      test_results.append(mixture_density_maximum_1d(np.array(tl_results)))
    else:
      test_results.append(0)

  return test_results

def RunTestSimplified(ds, file_path, time=5140, src_x=3, src_y=3):
  ds_data, timestamps = csv_to_array(txt_to_csv(file_path))
  z_values = MarkZValuesDirty(txt_to_csv(file_path), time, 8.5, 0)

  test_results = np.array(RunLocalizationTestSimplified(ds, ds_data, src_x, src_y))
  
  test_results_ts = np.column_stack((timestamps, z_values, test_results))
  array_to_csv(file_path[:-4] + '_simp_sq', test_results_ts, ['time', 'real_z', 'z'])

  return ('/content/' + file_path[9:-4] + '_simp_sq.csv')

# TEST LOG 1
def RunLocalizationTestSimplifiedLog(ds, ds_data, src_x, src_y):
  min_ds = 2
  test_results = []

  for i in range(len(ds_data[0])):
    # setting dosimeter radiation
    for j in range(len(ds)):
      radiation = float(ds_data[j][i])
      if (radiation > 0.0032):
        ds[j].radiation = radiation
      else:
        ds[j].radiation = 0
    radiation_to_distance_log(ds)

    no_zeros_ds = []
    for d in ds:
      if (d.radiation != 0):
        no_zeros_ds.append(d)

    # Calculating with exhaustinve trilateration
    tl_results = []
    combinations = list(itertools.combinations(no_zeros_ds, min_ds))
    for combo in combinations:
      try:
        tl_results.append(Trilateration3DSimplifiedLog(combo, src_x, src_y))
      except ZeroDivisionError:
        None

    # Calculating highest density value
    if (len(tl_results) > 0):
      test_results.append(mixture_density_maximum_1d(np.array(tl_results)))
    else:
      test_results.append(0)

  return test_results

def RunTestSimplifiedLog(ds, file_path, time=5150, src_x=3, src_y=3):
  ds_data, timestamps = csv_to_array(txt_to_csv(file_path))
  z_values = MarkZValuesDirty(txt_to_csv(file_path), time, 8.5, 0)

  test_results = np.array(RunLocalizationTestSimplifiedLog(ds, ds_data, src_x, src_y))
  
  test_results_ts = np.column_stack((timestamps, z_values, test_results.T))
  array_to_csv(file_path[9:-4] + '_simp_log', test_results_ts, ['time', 'real_z', 'z'])

  return ('/content/' + file_path[9:-4] + '_simp_log.csv')

# TEST LOG 2
def RunLocalizationTestLogAlt(ds, ds_data):
  min_ds = 4 # minimum number of dosimeters
  test_results = []

    # # setting dosimeter radiation
    # for j in range(len(ds)):
    #   radiation = float(ds_data[j][i])
    #   if (radiation > 0.0032):
    #     ds[j].radiation = radiation
    #   else:
    #     ds[j].radiation = 0
    
  clear_radiation_noise(ds, ds_data)
  # for each dosimeter
  for i in range(len(ds_data[0])):
    radiation_to_distance_log(ds)

    no_zeros_ds = []
    for d in ds:
      if (d.radiation != 0):
        no_zeros_ds.append(d)

    # Calculating with exhaustinve trilateration
    tl_results = []
    combinations = list(itertools.combinations(no_zeros_ds, min_ds))
    for combo in combinations:
      try:
        res = Trilateration3D(combo)
        tl_results.append(res)
      except ZeroDivisionError:
        None

    # Calculating highest density value
    if (len(tl_results) > 0):
      test_results.append(mixture_density_maximum_3d(np.array(tl_results)))
    else:
      test_results.append([0,0,0])

  return test_results

def RunTestLogAlt(ds, file_path, time=5150):
  ds_data, timestamps = csv_to_array(txt_to_csv(file_path))
  z_values_dirty = MarkZValuesDirty(txt_to_csv(file_path), time, 8.5, 0)
  z_values_clean = MarkZValuesDeprecated(txt_to_csv(file_path), time, 8.5, 0)

  test_results = np.array(RunLocalizationTestLogAlt(ds, ds_data))
  
  test_results_ts = np.column_stack((timestamps, z_values_dirty, z_values_clean, test_results.T[0],  test_results.T[1], test_results.T[2]))
  array_to_csv(file_path[9:-4] + '_log', test_results_ts, ['time', 'real_z', 'clean_z', 'x', 'y', 'z'])

  return ('/content/' + file_path[9:-4] + '_log.csv')





