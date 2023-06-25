import matplotlib.pyplot as plt
import numpy as np
from scipy.special import comb
import json


def get_bezier_parameters(X, Y, degree=3):
    """ Least square qbezier fit using penrose pseudoinverse.

    Parameters:

    X: array of x data.
    Y: array of y data. Y[0] is the y point for X[0].
    degree: degree of the Bézier curve. 2 for quadratic, 3 for cubic.

    Based on https://stackoverflow.com/questions/12643079/b%C3%A9zier-curve-fitting-with-scipy
    and probably on the 1998 thesis by Tim Andrew Pastva, "Bézier Curve Fitting".
    """
    if degree < 1:
        raise ValueError('degree must be 1 or greater.')

    if len(X) != len(Y):
        raise ValueError('X and Y must be of the same length.')

    if len(X) < degree + 1:
        raise ValueError(f'There must be at least {degree + 1} points to '
                         f'determine the parameters of a degree {degree} curve. '
                         f'Got only {len(X)} points.')

    def bpoly(n, t, k):
        """ Bernstein polynomial when a = 0 and b = 1. """
        return t ** k * (1 - t) ** (n - k) * comb(n, k)
        # return comb(n, i) * ( t**(n-i) ) * (1 - t)**i

    def bmatrix(T):
        """ Bernstein matrix for Bézier curves. """
        return np.matrix([[bpoly(degree, t, k) for k in range(degree + 1)] for t in T])

    def least_square_fit(points, M):
        M_ = np.linalg.pinv(M)
        return M_ * points

    T = np.linspace(0, 1, len(X))
    M = bmatrix(T)
    points = np.array(list(zip(X, Y)))

    final = least_square_fit(points, M).tolist()
    final[0] = [X[0], Y[0]]
    final[len(final)-1] = [X[len(X)-1], Y[len(Y)-1]]
    return final


def bernstein_poly(i, n, t):
    """
     The Bernstein polynomial of n, i as a function of t
    """
    return comb(n, i) * (t**(n-i)) * (1 - t)**i


def bezier_curve(points, nTimes=50):
    """
       Given a set of control points, return the
       bezier curve defined by the control points.

       points should be a list of lists, or list of tuples
       such as [ [1,1], 
                 [2,3], 
                 [4,5], ..[Xn, Yn] ]
        nTimes is the number of time steps, defaults to 1000

        See http://processingjs.nihongoresources.com/bezierinfo/
    """
    nPoints = len(points)
    xPoints = np.array([p[0] for p in points])
    yPoints = np.array([p[1] for p in points])

    t = np.linspace(0.0, 1.0, nTimes)

    polynomial_array = np.array(
        [bernstein_poly(i, nPoints-1, t) for i in range(0, nPoints)])

    xvals = np.dot(xPoints, polynomial_array)
    yvals = np.dot(yPoints, polynomial_array)

    return xvals, yvals


# Abrimos el archivo json original
with open('//json/roads.json') as infile:
    json_info = json.load(infile)  # Accedemos a la info del json

json_colls = json_info['Roads']  # Cogemos las colecciones de la info del json
# coll_name coge Road0, Road1, Road2....
# coll_info coge la info de dentro de estos dos: Directions y Points

data_json = {}
data_json['Roads']=[]
n = 0

for coll_name, coll_info in json_colls.items():
    pointsX = []
    poinstY = []
    for point1, point2 in coll_info['Points']:
        #Creamos un vector con los puntos de una carretera
        pointsX.append(point1)
        poinstY.append(point2)

    direct_reverse = []
    for carriles_name, carriles_info in coll_info['Directions'].items():
        print(carriles_name)  # Nos da Direct y Reverse
        # print(carriles_info) #Nos da el Integer
        direct_reverse.append(carriles_info)

    
    new_points = get_bezier_parameters(pointsX, poinstY, 3)
    data_json['Roads'].append({
    'Road' + str(n):{ 
        'Directions':{
            'Direct': direct_reverse[0],
            'Reverse': direct_reverse[1]
        },
        'Points': new_points
    } 
    })

    n+=1

#### Lo guardamos todo en un json
with open('//json/roads_bezier.json', 'w') as file:
    json.dump(data_json, file, indent=4)
