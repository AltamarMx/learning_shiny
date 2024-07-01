import numpy as np

def solve_1d_Tfree(dia):
    dia['Ti'] = dia.Ta + np.random.random()
    dia['Tsi'] = dia.Ta + np.random.random()
    dia['Tse'] = dia.Ta + np.random.random()
    return diaz