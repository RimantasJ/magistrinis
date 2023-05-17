from global_variables import *
from th_math.math import *
from th_math.mixture_maximum import *
from th_math.trilateration import *
from th_formatting.formatting import *
from th_tests.tests import *

# TEST BASE
def calculate_coordinates(ds, ds_values):
    min_ds = 4
    test_results = np.zeros((len(ds_values), 3), dtype=float)

    for i, radiations in enumerate(ds_values):
        # Only start when all dosimeters have detected radiation above threshold
        if np.count_nonzero(radiations) != ds.size:
            continue
        
        # Calculate dosimeters distance to source
        # radiation_to_distance_nth_root(ds, radiations, 2)
        radiation_to_distance_log(ds, radiations)

        # Calculate coordinates using different combinations of dosimeters
        tl_results = []
        dosimeter_combinations = list(itertools.combinations(ds, min_ds))
        for combo in dosimeter_combinations:
            try:
                temp = trilateration_3d_abs(combo)
                tl_results.append(temp)
            except ZeroDivisionError:
                None

        # Calculate most probable coordinates
        if (len(tl_results) > 0):
            test_results[i] = mixture_density_maximum_3d(np.array(tl_results))

    return test_results

def TestRunner(ds, file_path):
    csv_file_path = txt_to_csv(file_path)
    timestamps, ds_values  = csv_to_array(csv_file_path) 
    
    clear_radiation_noise(ds_values, 0.0032)
    calculated_coordinates = calculate_coordinates(ds, ds_values)
    
    real_coordinates = get_real_coordinates(timestamps, ds_values, 8.5)
    
    result_path = 'results/' + file_path[5:-4] + '_res'
    
    # test_results = np.column_stack((real_src_coordinate, calculated_coordinates.T[0],  calculated_coordinates.T[1], calculated_coordinates.T[2]))
    array_to_csv(result_path, ['time', 'correct_z', 'x', 'y', 'z'], timestamps, real_coordinates, calculated_coordinates)
    # return test_results
    
# MandatoryLast
print("Starting test run:")
TestRunner(ds, 'data/test25sample.txt')
print("Finnished test run")