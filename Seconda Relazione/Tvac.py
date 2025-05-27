import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

header_to_skip = 155
file_path = "Data/Tvac.txt"

class TvacTest():
    def __init__(self):
        self.columns = {}
    def create_columns(self):
        column_names = (np.genfromtxt(file_path, skip_header = header_to_skip, max_rows = 1, delimiter="\t", dtype=str)).tolist()
    
        for i in range(len(column_names)):
            self.columns[column_names[i]] = (np.genfromtxt(file_path, skip_header = header_to_skip+1, usecols=(i), delimiter="\t", dtype=str)).tolist()
        return self.columns
    
    def trend(self, data, column_name):
        values = data[column_name]
        response = []

        if column_name == "Date Time":
            values = [datetime.strptime(data_str, "%d/%m/%y %H:%M:%S") for data_str in values]
            return values
        else:
            values = np.asarray(data[column_name]).astype(float)

            for element in range(len(values) - 1):
                if (-0.099 <= values[element] - values[element+1] <= 0.099):
                    response.append(0) #stabile
                elif (values[element] - values[element+1] > 0.099):
                    response.append(-20) #decresce
                elif (values[element] - values[element+1] < -0.099):
                    response.append(20) #aumenta
            return response

    def create_array(self, data, column_name):
        values = data[column_name]

        if column_name == "Date Time":
            values = [datetime.strptime(data_str, "%d/%m/%y %H:%M:%S") for data_str in values]
            return values
        else:
            values = np.asarray(data[column_name]).astype(float)
            return values

def plot_data(x_data, y_data, x_label="X", y_label="Y", title="Grafico"):
    plt.plot(x_data, y_data, linestyle='-', color='b')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(True)
    plt.show()

def comparison(value1, value2, label1, label2, scale = False):
    plt.figure(figsize=(12, 6))
    plt.plot(date_time, value1, linestyle='-', color='b', label=label1)
    plt.plot(date_time, value2, linestyle='-', color='r', label = label2)
    plt.xlabel('Date Time')
    plt.ylabel(f"{label1} vs {label2}")
    if scale:
        plt.yscale("log")
    plt.legend()
    plt.grid(True)
    plt.show()

tvac = TvacTest()
data = tvac.create_columns()

trend = tvac.trend(data, "T Shroud")
date_time = tvac.trend(data, "Date Time")
plot_data(date_time[:-1], trend, x_label="Date Time", y_label= "T Shroud", title="Trend T Shroud")

t_shroud = tvac.create_array(data, "T Shroud")
t_shroud_setpoint = tvac.create_array(data, "T Shroud Setpoint")
comparison(t_shroud, t_shroud_setpoint, "t_shroud", "t_shroud_setpoint")


P_Full_Range_1_chamber_ITR90 = tvac.create_array(data, "P Full Range 1 chamber-ITR90")
P_Chamber = tvac.create_array(data, "P Chamber")
comparison(P_Full_Range_1_chamber_ITR90, P_Chamber, "P Full Range 1 chamber-ITR90", "P_Chamber", scale=True)

