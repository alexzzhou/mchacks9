import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 

rail_data = pd.read_csv('rail_data.csv')

print(rail_data.head())

rail_data.plot(x="Time",)

plt.show()