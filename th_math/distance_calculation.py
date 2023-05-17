from th_math.math import *
from global_variables import *

# ------------------------
#  Radiation to distance
# ------------------------

def radiation_to_distance_nth_root(ds, radiations, n):
    for i, r in enumerate(radiations):
        if (r != 0):
            ds[i].distance = 1 / (r ** (1 / n))  

def radiation_to_distance_log(ds, radiations, ds_ab=DS_AB_PRECALC):
    # could use FitRadiationExpWithData
    for i, r in enumerate(radiations):
        if (r != 0):
            ds[i].distance = np.log(r / ds_ab[i][0]) / ds_ab[i][1]




def fit_radiation_exp_with_data(first_file, last_file, dosimeter_number):
    distances = np.array([], dtype=float)
    radiations = np.array([], dtype=float)

    for i in range(first_file, last_file+1):
        temp_distances, temp_radiations = map_distance_to_radiation(i, dosimeter_number)
        distances = np.append(distances, temp_distances)
        radiations =  np.append(radiations, temp_radiations)

    a, b = FitTwoLists(distances, radiations)
    return a, b

def map_distance_to_radiation(test_number, dosimeter_number):
    dosimeter = Dosimeter3D(x=TestNumberToXCoordinate(test_number), z=DosimeterNumberToZCoordinate(dosimeter_number+1))
    csv_file_path = '/content/test' + str(test_number) + '.csv'

    src_z_values = MarkZValuesDeprecated(csv_file_path, 2140, 8.5, dosimeter_number)
    d_to_src_distances = CalcDosimeterToSourceDistances(dosimeter, src_z_values)
    ds_radiation, timestamps = CsvToDosimeterDataArray(csv_file_path)
    d_radiation, d_to_src_distances = RemoveZeroValuesFromLists(ds_radiation[dosimeter_number], d_to_src_distances)

    d_radiation_float = np.zeros(len(d_radiation))
    for i in range(len(d_radiation)):
        d_radiation_float[i] = float(d_radiation[i])

    return d_to_src_distances, d_radiation_float


def TestNumberToXCoordinate(num):
    if (num > 16):
        num -= 14
    elif (num > 9):
        num -= 7
    num -= 3
    return num

def DosimeterNumberToZCoordinate(num):
    z = 2
    if (num % 3 == 2):
        z += 3
    elif (num % 3 == 0):
        z += 6
    return z

# Calcualtes Euclidean distances from dosimeter to source
def CalcDosimeterToSourceDistances(dosimeter, src_z_values, src_x = 0):
    distances_list = np.zeros(len(src_z_values))

    for i in range(len(src_z_values)):
        if (src_z_values[i] != 0):
            distances_list[i] = math.sqrt((src_z_values[i] - dosimeter.z)**2 + (src_x - dosimeter.x)**2) 

    return distances_list

def FitTwoLists(xs, ys):
    [a, b], res1 = curve_fit(lambda x1,a,b: a * np.exp(b * x1),  xs,  ys)
    return a, b








