from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

#-------------------------------------
# 1. DEFINE DIRECTORIES AND LOAD DATA
#-------------------------------------
# PROJECT_DIR is the root of the project (assumes this script is run from there)
# DATA_DIR    holds the input .npz file
# RESULTS_DIR is created automatically if it doesn't exist yet

PROJECT_DIR = Path.cwd()  # only if the working directory is the project root
DATA_DIR = PROJECT_DIR / "data" # i save the generated dataset in the data folder
RESULTS_DIR = PROJECT_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

fc_file = DATA_DIR / "connectivity_matrices_clean.npz"
fc_data = np.load(fc_file)

fc_matrices_clean = fc_data["matrices"]

#--------------------------------------
# 2. Select one participant's FC matrix
#--------------------------------------
subject_idx = 7
FC_thresholded = fc_matrices_clean[subject_idx]

# define the ROI labels 
roi_names = [
    "mPFC", "PCC", "L_Angular", "R_Angular",
    "L_Insula", "dACC", "L_dlPFC", "R_dlPFC"
]

# --------------------
# 3. Build the graph 
# --------------------
# Each ROI becomes a node; each surviving (non-zero) FC value becomes a
# weighted, undirected edge. We iterate over the upper triangle only to
# avoid adding duplicate edges from the symmetric matrix.

G = nx.Graph()
G.add_nodes_from(roi_names)

# place all nodes evenly around a circle so no edges are obscured by the layout

for i in range(len(roi_names)):
    for j in range(i + 1, len(roi_names)):
        weight = FC_thresholded[i, j]

        if weight != 0:
            G.add_edge(roi_names[i], roi_names[j], weight=weight)

# arrange the nodes in a circle
pos = nx.circular_layout(G)

# separate positive and negative connections
positive_edges = [
    (u, v) for u, v, d in G.edges(data=True)
    if d["weight"] > 0
]
negative_edges = [
    (u, v) for u, v, d in G.edges(data=True)
    if d["weight"] < 0
]

# scale line thickness by absolute FC strength
edge_widths = [
    abs(G[u][v]["weight"]) * 8
    for u, v in G.edges()
]

plt.figure(figsize=(10, 8))

nx.draw_networkx_nodes(
    G, pos, node_size=1800, node_color="lightblue"
)
nx.draw_networkx_labels(G, pos, font_size=9)

nx.draw_networkx_edges(
    G, pos, edgelist=positive_edges,
    edge_color="red",
    width=[
        abs(G[u][v]["weight"]) * 8
        for u, v in positive_edges
    ]
)

nx.draw_networkx_edges(
    G, pos, edgelist=negative_edges,
    edge_color="blue",
    style="dashed",
    width=[
        abs(G[u][v]["weight"]) * 8
        for u, v in negative_edges
    ]
)

plt.title(f"FC Network — Participant {subject_idx + 1} ")
plt.axis("off")
plt.tight_layout()

# --------------------------------------
# 4. Save the figure 
# --------------------------------------
# It is important to save the figure before showing it!

output_path = PROJECT_DIR / "results" / f"fc_network_participant_{subject_idx + 1}.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight")
print(f"Figure saved to: {output_path}")

plt.show()