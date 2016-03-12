
/**************************************************************************
** CLSDBC: C version for Locally Scaled Density Based Clustering
** 
** Version: 1.0
** 
** Author: Ergun Bicici
**
** Date: 19/07/2006
***************************************************************************/

/* [clusts,noise] = LSDBC(D, k, n, alpha) 

% Given a similarity matrix for a number of points
% allocates all points to a cluster or specify them as noise
% D: Distance matrix
% k: k-dist parameter
% n: number of dimensions
*/

For compiling: 
gcc -o clsdbc clsdbc.c -lm

For debugging with kdgb: 
gcc -g -o clsdbc clsdbc.c -lm

Usage: %s matrix_file k alpha numDimensions 

[integer] k: Number of neighbors to consider (for kNN based density estimation).
[integer] alpha: Adjusting parameter for density cutoff. 
[integer] numDimensions: Number of dimensions the original data resides in. 
	  alpha = numDimensions --> Cluster number is changed once the density falls below the half of the original density.

Input matrix_file format: Dense text.

Example:

3
0   0.1	4.2
0.1 0	2.2
4.2 2.2	0
