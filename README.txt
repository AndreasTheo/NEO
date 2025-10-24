Abstract:
Efficient exploration remains one of the key open problems in reinforcement learning. Discovering novel states or transitions efficiently requires policies that effectively direct the agent away from regions of the state space that are already well explored. We introduce Novel Exploration via Orthogonality (NEO), an approach that automatically uncovers not only which regions of the environment are novel but also how to reach them by leveraging Laplacian representations. NEO uses the eigenvectors of a modified graph Laplacian to induce gradient flows from states that are frequently visited (less novel) to states that are seldom visited (more novel). We show that NEO’s modified Laplacian yields eigenvectors whose extreme values align with the most novel regions of the state space. We provide bounds for the eigenvalues of the modified Laplacian; and we show that the smoothest eigenvectors with real eigenvalues below certain thresholds provide guaranteed gradients to novel states for both undirected and directed graphs. In an empirical evaluation in online, incremental settings, NEO outperformed related state-of-the- art approaches, including eigen-options and cover options, in a large collection of undirected and directed domains with varying structures.

To run the empirical experiments, run the code in:
Main_Evals.ipynb for all domains except the NYC domain, and run the code in:
NYC_Street_Evals.ipynb for the NYC domain.

After running the code, plots are created in the file:
Plots.ipynb

