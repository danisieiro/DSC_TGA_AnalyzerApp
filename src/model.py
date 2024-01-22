from scipy.signal import find_peaks, argrelextrema
import numpy as np
import pandas as pd

class ThermalAnalysis:

    __area: tuple[int, int, int]

    def __init__(self, data):

        data.drop(0, inplace=True)
        data['HF/M'] = data['HF'] / data['Weight'][1]
        data['% mass'] = 100 * data['Weight'] / data['Weight'][1]
        data.reset_index(drop=True, inplace=True)

        self.__data = data
        self.__area = self.area()
        self.__onset = {
            'temperature': 0,
            '% mass': 0,
            'intercept 1': 0,
            'intercept 2': 0,
            'slope 1': 0,
            'slope 2': 0
        }
        self.__transition_mass = {
            'First transition': 0,
            'Second transition': 0
        }
        self.__peaks = 0


    def get_data(self):

        return self.__data

    def get_area(self):

        return self.__area

    def get_onset(self):

        return self.__onset

    def area(self, conversion=6):

        data = self.__data

        total = 0
        endo = 0
        exo = 0

        for i in range(len(data['Ts']) - 1):
            deltat = data['Ts'][i + 1] - data['Ts'][i]
            suma = deltat * (data['HF/M'][i] + data['HF/M'][i + 1]) / 2
            total += suma

            if suma <= 0:
                exo += suma

            else:
                endo += suma

        self.__area = (conversion * total, conversion * endo, conversion * exo)
        return self.__area

    def residual(self, t):

        data = self.__data

        temperature = np.array(data['Ts'])

        closest_temperature = min(temperature, key=lambda x: abs(x - t))

        res = float(data.loc[data['Ts'] == closest_temperature]['% mass'])

        return closest_temperature, res

    def find_dsc_peaks(self, prominence=0.5):

        # Encuentra los picos usando scipy find_peaks
        peaks, _ = find_peaks(-self.__data['HF/M'], prominence=prominence)

        return peaks

    def find_transition_points(self, selected_interval):

        # Calcular la primera derivada de la curva TGA
        derivative = np.abs(pd.Series(np.gradient(self.__data['% mass'])))

        # Obtiene el indice de los puntos en los que la derivada se hace minima o maxima
        mass1_index = derivative[selected_interval[0]:selected_interval[1]].idxmin()
        mass2_index = derivative[selected_interval[1]:selected_interval[2]].idxmax()
        mass3_index = derivative[selected_interval[2]:selected_interval[3]].idxmin()
        mass4_index = derivative[selected_interval[3]:selected_interval[4]].idxmax()
        mass5_index = derivative[selected_interval[4]:selected_interval[5]].idxmin()


        return (mass1_index, mass2_index, mass3_index, mass4_index, mass5_index)

    def calculate_tga_deltam(self, selected_interval):

        index = self.find_transition_points(selected_interval)

        delta_m1 = self.__data['% mass'][index[0]] - self.__data['% mass'][index[2]]
        delta_m2 = self.__data['% mass'][index[2]] - self.__data['% mass'][index[4]]

        self.__transition_mass = {
            'First transition': delta_m1,
            'Second transition': delta_m2
        }

        return (delta_m1, delta_m2)

    def calculate_onset(self, selected_interval):

        index = self.find_transition_points(selected_interval)

        temperature_1 = self.__data['Ts'][index[2]]
        temperature_2 = self.__data['Ts'][index[3]]

        # Obtenemos la derivada de % mass
        derivative = np.gradient(self.__data['% mass'], self.__data['Ts'])

        # Almacenamos el valor de las pendientes
        m1 = derivative[index[2]]
        m2 = derivative[index[3]]

        # Almacenamos el valor de los terminos independientes
        n1 = self.__data['% mass'][index[2]] - m1 * temperature_1
        n2 = self.__data['% mass'][index[3]] - m2 * temperature_2

        # Calculamos el punto de corte (onset) entre las dos gráficas
        onset_temperature = (n1 - n2) / (m2 - m1)
        onset_mass = n1 + onset_temperature * m1

        self.__onset = {
            'temperature': onset_temperature,
            '% mass': onset_mass,
            'intercept 1': n1,
            'intercept 2': n2,
            'slope 1': m1,
            'slope 2': m2
        }

        return self.__onset