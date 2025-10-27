
# Written by Ryan Cerauli for the DAN Research Program headed by Anthony F. Beavers @ Indiana University. Copyright 2024. 
# See https://www.afbeavers.net/drg for more information


import numpy as np
from Dataset import theData, categoryDict
import copy


# Note: This file was written almost exclusively with the assistance of AI for readability and out of laziness


# --------------------------
# 1. Compression function
# --------------------------
def compress_dataset_orthonormal(A, b):
    """
    Compresses dataset A, b using an orthonormal row basis.
    
    Returns:
        row_basis_ortho : orthonormal row basis (r x n_features)
        coeffs_A        : coefficients to reconstruct all rows (n_rows x r)
        b_basis         : outputs corresponding to independent rows (r,)
        independent_rows: indices of rows chosen as basis
    """
    # Find independent rows
    independent_rows = []
    for i in range(A.shape[0]):
        candidate = A[independent_rows + [i], :] if independent_rows else A[[i], :]
        if np.linalg.matrix_rank(candidate) > len(independent_rows):
            independent_rows.append(i)

    row_basis = A[independent_rows, :]
    r = len(row_basis)

    # Orthonormalize row basis using QR
    Q, R = np.linalg.qr(row_basis.T)
    row_basis_ortho = Q.T  # shape r x n_features

    # Compute coefficients for reconstructing all rows
    coeffs_A = np.zeros((A.shape[0], r))
    for j in range(A.shape[0]):
        coeffs_A[j] = np.linalg.lstsq(row_basis_ortho.T, A[j].reshape(-1,1), rcond=None)[0].flatten()

    # Outputs of the basis rows
    b_basis = b[independent_rows]

    return row_basis_ortho, coeffs_A, b_basis, independent_rows

# --------------------------
# 2. Reconstruction function
# --------------------------
def reconstruct_outputs(x, row_basis_ortho, coeffs_A, retrieveOutputVector=True):
    """
    Reconstructs outputs for a new input vector x using the orthonormal compressed dataset.
    """
    y_compressed = row_basis_ortho @ x
    if not retrieveOutputVector:
        return coeffs_A @ y_compressed
    else:
        theNewData = copy.deepcopy(dataListMinusOutput)
        DANOutput = (coeffs_A @ y_compressed).tolist()
        for clusterIndex in range(len(dataListMinusOutput)):
            for element in range(len(dataListMinusOutput[clusterIndex])):
                theNewData[clusterIndex][element] = theNewData[clusterIndex][element] * DANOutput[clusterIndex]
        finalOutputVector = []
        for elementIndex in range(len(theNewData[0])):
            outputHolder = []
            for newClusterIndex in range(len(theNewData)):
                outputHolder.append(theNewData[newClusterIndex][elementIndex])
            maxVal = max(outputHolder)
            finalOutputVector.append(maxVal)
        return finalOutputVector


# --------------------------
# 3. Example usage
# --------------------------
if __name__ == "__main__":

    retrieveOutputVectorBool = True
    dataListMinusOutput = []
    outputVector = []
    for dataCluster in theData:
        newCluster = dataCluster[:-1]
        output = dataCluster[-1]
        dataListMinusOutput.append(newCluster)
        outputVector.append(output) 

    A = np.array(dataListMinusOutput, dtype=float)

    b = np.array(outputVector, dtype=float) 

    # Compress dataset
    row_basis_ortho, coeffs_A, b_basis, independent_rows = compress_dataset_orthonormal(A, b) 

    # Test with a new input
    x = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0], dtype=float)
    if retrieveOutputVectorBool:
        newNewData = copy.deepcopy(dataListMinusOutput)
        DANOutput = []
        otherx = x.tolist()
        for cluster in range(len(newNewData)):
            sum = 0
            for element in range(len(newNewData[cluster])):
                sum += otherx[element] * newNewData[cluster][element]
            DANOutput.append(sum)
        for clusterIndex in range(len(newNewData)):
            for element in range(len(newNewData[clusterIndex])):
                newNewData[clusterIndex][element] = newNewData[clusterIndex][element] * DANOutput[clusterIndex]
        finalOutputVector = []
        for elementIndex in range(len(newNewData[0])):
            outputHolder = []
            for newClusterIndex in range(len(newNewData)):
                outputHolder.append(newNewData[newClusterIndex][elementIndex])
            maxVal = max(outputHolder)
            finalOutputVector.append(maxVal)
        b_original = finalOutputVector
    else:
        b_original = A @ x
    b_reconstructed = reconstruct_outputs(x, row_basis_ortho, coeffs_A, retrieveOutputVector=retrieveOutputVectorBool) 
    differenceVector = []
    for i in range(len(b_original)):
        b_reconstructed[i] = b_reconstructed[i]/(len(categoryDict)) 
        b_original[i] = b_original[i]/(len(categoryDict)) ########wjehdfvjsowieuhrfgbndspwehfgvnpwoejhfjk############
    for element in range(len(b_original)):
        differenceVector.append(round(b_original[element] - b_reconstructed[element], 10)) 
        pass

    # Results
    print("Original row count:", len(A), "\n")
    print("New row count:", len(independent_rows), "\n") 
    print("Orthonormal row basis:", row_basis_ortho, "\n") 
    print("Original outputs:      ", b_original, "\n")
    print("Reconstructed outputs: ", b_reconstructed, "\n") 
    print("Difference:            ", differenceVector, "\n")
