
# Verifying that the required libraries are installed.
import sys

import requests
import pandas as pd
import numpy as np
import dotenv
import matplotlib
import seaborn as sns
import jupyter
import ipykernel

# Display the Python executable used by this project.
print("Python executable:", sys.executable)

# Display installed library versions.
print("Requests:", requests.__version__)
print("Pandas:", pd.__version__)
print("NumPy:", np.__version__)
print("Matplotlib:", matplotlib.__version__)
print("Seaborn:", sns.__version__)
print("Environment check: SUCCESS")
