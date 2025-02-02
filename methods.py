import pandas as pd
from scipy.stats import linregress
import matplotlib.pyplot as plt
import numpy as np
from fitparse import FitFile
import csv
import os
import re

class Data:
    def __init__(self, df):
        self.df = df

class Generator:
    def __init__(self, fitDataPath, csvDataPath):
        self.fitDataPath = fitDataPath
        self.csvDataPath = csvDataPath

    def produceFits(self):

        with open('fits.csv', "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["name", "watts", "date", "expectedDrift","intercept", "r_value", "p_value", "std_err"])

            for filename in os.listdir(self.csvDataPath):
                if filename.endswith(".csv"):
                    # Extract name and watts using regex
                    match = re.match(r"(.+)_([\d]+)_([\d:-]+)\.csv", filename)   # Example: "Cesare_165_11:19:2024.fit"
                    if match:
                        name, watts, date = match.groups()
                        watts = int(watts)  # Convert watts to integer
                        print(name, watts)
                        expectedDrift, intercept, r_value, p_value, std_err, xRange, yPredicted = linearFit(self.csvDataPath + "/" + filename)
                        writer.writerow([name, watts, date, expectedDrift,intercept, r_value, p_value, std_err])
                    else:
                        print(f"Skipping file (invalid format): {filename}")
                        continue

    def createCSVs(self):
        for filename in os.listdir(self.fitDataPath):
            if filename.endswith(".fit"):
                # Extract name and watts using regex
                match = re.match(r"(.+)_([\d]+)_([\d:-]+)\.fit", filename)
                if match:
                    name, watts, date = match.groups()
                    watts = int(watts)  # Convert watts to integer
                    print(name, watts)
                    createCSV(self.fitDataPath + '/' + filename, 'csvFiles/' + name + '_' + str(watts) + '_' + date + '.csv')
                else:
                    print(f"Skipping file (invalid format): {filename}")
                    continue


@staticmethod
def displayLinearFit(filePath):

    createCSV(filePath, filePath[:-4] + ".csv")
    df = pd.read_csv(filePath[:-4] + ".csv")
    expectedDrift, intercept, r_value, p_value, std_err, xRange, yPredicted = linearFit(filePath[:-4] + ".csv")
    plt.figure(figsize=(10, 6))
    plt.title("Heart Rate Linear Regression")
    plt.plot(df['time'] / 60, df['heartRate'], color='red', label='Heart Rate')
    plt.plot(xRange / 60, yPredicted, color='blue', label=f'Drift : {expectedDrift:.1f} (over an hour)\n'
                                                          f'Error : {std_err:.2f} (over an hour)\n'
                                                          f'Intercept : {intercept:.2f}\n')
    plt.xlabel('Time (min)')
    plt.ylabel('Heart Rate')
    plt.legend()
    plt.tight_layout()
    plt.show()


@staticmethod
def linearFit(filePath):
    df = pd.read_csv(filePath)
    slope, intercept, r_value, p_value, std_err = linregress(df['time'], df['heartRate'])
    xRange = np.linspace(df['time'].min(), df['time'].max(), 100)
    yPredicted = slope * xRange + intercept
    expectedDrift = slope * 60 * 60
    return expectedDrift, intercept, r_value, p_value, std_err*60*60, xRange, yPredicted

@staticmethod
def createCSV(filePath, savePath):
    fit_file = FitFile(filePath)

    heartRate = []
    cadence = []
    power = []
    timeStamps = []

    for record in fit_file.get_messages("record"):
        data = {}
        for field in record:
            if field.name == 'cadence':
                cadence.append(float(field.value))
            elif field.name == 'heart_rate':
                heartRate.append(float(field.value))
            elif field.name == 'power':
                power.append(float(field.value))
            elif field.name == 'timestamp':
                timeStamps.append(float(field.value.timestamp()))

    power = np.array(power)
    cadence = np.array(cadence)
    heartRate = np.array(heartRate)
    timeStamps = np.array(timeStamps) - min(timeStamps)

    tenIn, tenOut = min(timeStamps) + 10 * 60, max(timeStamps) - 10 * 60
    aboveTenIndices = np.where(timeStamps > tenIn)[0]
    newStart = aboveTenIndices[0] if aboveTenIndices.size > 0 else None
    belowTenIndices = np.where(timeStamps < tenOut)[0]
    newEnd = belowTenIndices[-1] if belowTenIndices.size > 0 else None

    with open(savePath, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["power", "heartRate", "cadence", "time"])
        for power, heartRate, cadence, time in zip(power[newStart:newEnd], heartRate[newStart:newEnd],
                                                   cadence[newStart:newEnd], timeStamps[newStart:newEnd]):
            writer.writerow([power, heartRate, cadence, time])

@staticmethod
def seeFile(filePath):
    fit_file = FitFile(filePath)
    for record in fit_file.get_messages("record"):
        data = {}
        for field in record:
            data[field.name] = field.value
        print(data)