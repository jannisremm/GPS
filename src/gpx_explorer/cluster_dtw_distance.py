import hdbscan
import matplotlib.pyplot as plt
import numpy as np

distances = np.load("dtw_distances.npy")

# Instantiate HDBSCAN with precomputed metric
clusterer = hdbscan.HDBSCAN(metric="precomputed")

clusterer.fit(distances)

clusterer.condensed_tree_.plot()

plt.show()
