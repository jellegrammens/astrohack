import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.linear_model import LinearRegression


def isSpiral(row):
    if row['sphericity'] < 0.65:
        return True
    elif row['volatility'] > 2:
        return True
    else:
        return False


def flux_conversion(row):
    return np.log10(row.flux * 3.631 * 10.0**-6 * 10.0**-26 * 4 * np.pi * (row.Distance * 3.086 * 10**22)**2)


def calculate_coefficients():
    train0 = pd.read_csv('/Users/elissamatton/astro/results/batched/Train/features.csv', names=['SDSS_ID', 'sphericity', 'flux', 'volatility'], delimiter='  ')
    train1 = pd.read_csv('./Users/elissamatton/astro/results/batched/Train/Train_cleaned.csv', names=['SDSS_ID', 'logMstar', 'err_logMstar', 'Distance'], delimiter=';')
    # print train0.head()
    # print train1.head()
    joinedData = train0.merge(train1, how='inner', on=['SDSS_ID'])
    joinedData['flux_good'] = joinedData.apply(flux_conversion, axis=1)
    joinedData['is_spiral'] = joinedData.apply(isSpiral, axis=1)
    sphericals = joinedData[joinedData['is_spiral'] == False]
    spirals = joinedData[joinedData['is_spiral'] == True]
    c = 40000
    x_spherical_train = np.array(sphericals['flux_good'][:c])
    y_spherical_train = np.array(sphericals['logMstar'][:c])
    x_spiral_train = np.array(spirals['flux_good'][:c])
    y_spiral_train = np.array(spirals['logMstar'][:c])
    model_spiral = np.polyfit(x_spherical_train, y_spherical_train, deg=4, rcond=None, full=False, w=None, cov=False)
    model_spherical = np.polyfit(x_spherical_train, y_spherical_train, deg=4, rcond=None, full=False, w=None, cov=False)
    return [model_spiral, model_spherical]


# x_spirals = np.linspace(15, 25)
# y_spirals = np.array([polynomial(x, spiral_model) for x in x_spirals])
# x_sphericals = np.linspace(15, 25)
# y_sphericals = np.array([polynomial(x, spherical_model) for x in x_sphericals])
# spiralPlot = plt.scatter(np.array(spirals['flux_good']),np.array(spirals['logMstar']))
# spiralModel = plt.plot(x_spirals, y_spirals)
# plt.show()
# sphericalPlot = plt.scatter(np.array(sphericals['flux_good']),np.array(sphericals['logMstar']))
# sphericalModel = plt.plot(x_sphericals, y_sphericals)
# plt.show()
