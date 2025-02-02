import methods
import pandas as pd
import matplotlib.pyplot as plt

methods.displayLinearFit('singleExample/Cesare_165_1-30-2025.fit')

# gen = methods.Generator('fitFiles', 'csvFiles')
# gen.createCSVs()
# gen.produceFits()
#
# file_path = "fits.csv"
# df = pd.read_csv(file_path)
# df['date'] = pd.to_datetime(df['date'])
# df = df.sort_values(by='date')
#
# df = df[(df['watts'] == 165)]
# plt.figure(figsize=(10,8))  # Optional: Adjust figure size
# plt.plot(df['date'], df['expectedDrift'])
# plt.xlabel("Date")
# plt.ylabel("Expected Drift")
# plt.title("Expected Drift Over Time")
# plt.xticks(rotation=45)
# plt.grid(True)
# plt.tight_layout()
# plt.show()


