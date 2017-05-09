import numpy as np
import pandas as pd
import glob
from regression import calculate_coefficients, flux_conversion

# coeffs = calculate_coefficients()
# print 'spiral ' + coeffs[0]
# print 'spherical ' + coeffs[1]

# coefficients as extracted above are:
spiral_model = np.array([-9.95446201e-02, 8.08585626e+00, -2.45568769e+02, 3.30502647e+03, -1.66234332e+04])
# spiral_model = np.array(coeffs[0])
spherical_model = np.array([-4.33506227e-02, 3.49557380e+00, -1.05289621e+02, 1.40466733e+03, -6.99694016e+03])
# spherical_model = np.array(coeffs[1])

distances_file = pd.read_csv('/Users/elissamatton/astro/AstroData/Test_clean.csv', delimiter=';')


def stack_pandas():
    path = r'/Users/elissamatton/astro/results/batched/Test'  # use your path
    allFiles = glob.glob(path + "/*.csv")
    list_ = []
    for file_ in allFiles:
        df = pd.read_csv(file_, delimiter=',', header=None, names=['SDSS_ID', 'sphericity', 'flux', 'volatility'])
        list_.append(df)
    features = pd.concat(list_)
    return features


def polynomial_spherical(row):
    res = 0
    x = row['flux_good']
    for exponent in range(len(spherical_model)):
        res = res + spherical_model[exponent]*np.power(x, 4-exponent)
    return res


def polynomial_spiral(row):
    res = 0
    x = row['flux_good']
    for exponent in range(len(spiral_model)):
        res = res + spiral_model[exponent]*np.power(x, 4-exponent)
    return res


test_data = stack_pandas().merge(distances_file, on=['SDSS_ID'], how='inner')
test_data['flux_good'] = test_data.apply(flux_conversion, axis=1)
test_data['predicted_mass_spherical'] = test_data.apply(polynomial_spherical, axis=1)
test_data['predicted_mass_spiral'] = test_data.apply(polynomial_spiral, axis=1)
test_data['predicted_mass'] = test_data.apply(lambda x: x['predicted_mass_spherical'] if x['predicted_mass_spherical'] else x['predicted_mass_spiral'], axis=1)
test_data.to_csv('/Users/elissamatton/astro/results/predicted/test_predicted.csv', columns=['SDSS_ID', 'predicted_mass'], index=False)
