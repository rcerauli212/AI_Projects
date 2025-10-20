import numpy as np
from tqdm import tqdm
import math
from Dataset import theData
import DENNMatrices
import copy




################################################
### Construct Neural Network Equation Solver ###
################################################

def NNEquationSolver(DataMemberList, function="exponential", conditionNumber=False, compressToANN=False, leastSquareSolutionNorm=True, ridgeRegression=False, lambdaVar=0, normalizeOutputs=True, maxAlignment=True, linearCompression=True, nonLinearCompression=False):
    
    ######################################################################
    ### Construct Output Vector and Data Member List Excluding Outputs ###

    outputVectorDict = {}
    for column in range(len(DataMemberList[-1][-1])):
        outputVectorDictHolder = []
        for dataCluster in range(len(DataMemberList)):
            outputVectorDictHolder.append(DataMemberList[dataCluster][-1][column])
        outputVectorDict[f"Output {column + 1}: "] = outputVectorDictHolder
    DataListMinusOutput = []

    if compressToANN:
        if linearCompression:
            originalDataMemberList = copy.deepcopy(DataMemberList)
            otherOriginalDataMemberList = copy.deepcopy(DataMemberList)
            for item in originalDataMemberList:
                item.pop(-1)
            for item in otherOriginalDataMemberList:
                item.pop(-1)  
            Ab = np.array(otherOriginalDataMemberList, dtype=float)
            A = Ab[:, :]
            for key in outputVectorDict.keys():
                outputVectorDict[key] = np.array(outputVectorDict[key], dtype=float)
            r = np.linalg.matrix_rank(A)
            U, S, Vt = np.linalg.svd(A, full_matrices=False)
            row_basis = Vt[:r, :]
            coeffs = np.linalg.lstsq(row_basis.T, A.T, rcond=None)[0].T
            compressed_rows = []
            for i in range(r):
                row = np.zeros(A.shape[1])
                for j in range(A.shape[0]):
                    row += coeffs[j, i] * A[j]
                compressed_rows.append(row)
            compressed_rows = np.array(compressed_rows)
            for key in outputVectorDict.keys():
                outputVectorDict[key] = coeffs.T @ outputVectorDict[key]
            DataMemberList = compressed_rows.tolist()
            for key in outputVectorDict.keys():
                outputVectorDict[key] = outputVectorDict[key].tolist()
            for item in DataMemberList:
                DataListMinusOutput.append(item)
    

    else:
        for dataCluster in DataMemberList:
            newCluster = dataCluster[:-1]
            DataListMinusOutput.append(newCluster)
    
    

    #######################################
    ### Constructing Coefficient Matrix ###

    if not compressToANN:
        coefficientMatrix = []
        for inputDataCluster in tqdm(DataListMinusOutput):
            finalEquation = []
            for iterativeDataCluster in DataListMinusOutput:
                dotProductSum = 0
                for index in range(len(inputDataCluster)):
                    dotProductSum += inputDataCluster[index] * iterativeDataCluster[index]
                ### insert function "if" statements here ###
                if function == "":
                    finalEquation.append(dotProductSum)
                elif function == "exponential":
                    if dotProductSum > 0:
                        finalEquation.append(2**(dotProductSum/len(inputDataCluster)))
                    else:
                        finalEquation.append(-2**(-dotProductSum/len(inputDataCluster)))
                elif function == "sigmoid":
                    val = 1 / (1 + math.exp(-(dotProductSum/len(inputDataCluster))))
                    finalEquation.append(val)
                elif function == "tanh":
                    val = math.tanh(dotProductSum/len(inputDataCluster))
                    finalEquation.append(val)
                elif function == "relu":
                    val = max(0, dotProductSum/len(inputDataCluster))
                    finalEquation.append(val)

            coefficientMatrix.append(finalEquation)
            
    else:
        coefficientMatrix = []
        for inputDataCluster in tqdm(DataListMinusOutput):
            finalEquation = []
            for iterativeDataCluster in DataListMinusOutput:
                dotProductSum = 0
                for index in range(len(inputDataCluster)):
                    dotProductSum += inputDataCluster[index] * iterativeDataCluster[index]
                ### insert function "if" statements here ###
                if function == "":
                    finalEquation.append(dotProductSum)
                elif function == "exponential":
                    if dotProductSum > 0:
                        finalEquation.append(2**(dotProductSum/len(inputDataCluster)))
                    else:
                        finalEquation.append(-2**(-dotProductSum/len(inputDataCluster)))
                elif function == "sigmoid":
                    val = 1 / (1 + math.exp(-(dotProductSum/len(inputDataCluster))))
                    finalEquation.append(val)
                elif function == "tanh":
                    val = math.tanh(dotProductSum/len(inputDataCluster))
                    finalEquation.append(val)
                elif function == "relu":
                    val = max(0, dotProductSum/len(inputDataCluster))
                    finalEquation.append(val)

            coefficientMatrix.append(finalEquation)


    ##############################################################
    ### Construct Numpy Arrays for Solving System of Equations ###

    numpyCoefficientMatrix = np.array(coefficientMatrix)


    if conditionNumber:
        K = numpyCoefficientMatrix
        print("K shape:", K.shape)
        rank_K = np.linalg.matrix_rank(K)
        print("rank(K):", rank_K)
        try:
            condK = np.linalg.cond(K)
        except Exception:
            condK = float('inf')
        print("cond(K):", condK)

    #################################
    ### Solve System of Equations ###

    SolutionsDict = {}
    for outputVecKey, outputVec in outputVectorDict.items():
        numpyOutputVector = np.array(outputVec)
        if leastSquareSolutionNorm:
            Solutions = np.linalg.lstsq(numpyCoefficientMatrix, numpyOutputVector, rcond=None)
        elif ridgeRegression:
            n = numpyCoefficientMatrix.shape[1]
            Solutions = [np.linalg.solve(numpyCoefficientMatrix.T @ numpyCoefficientMatrix + lambdaVar * np.eye(n), numpyCoefficientMatrix.T @ numpyOutputVector)]
        SolutionsDict[outputVecKey] = Solutions[0]
        

    #############################################################################
    ### Define 1st Layer Matrix and 2nd Layer Matrix for the Class ###


    firstLayerMatrix = DataListMinusOutput
    secondLayerMatrixDict = SolutionsDict
    

    print("Number of Hidden Nodes: ", len(DataMemberList))

    ######################################
    ### Return Neural Network Matrices ###

    return firstLayerMatrix, secondLayerMatrixDict, function


################################
### Construct DAN->ANN Class ###
################################

class DANtoANNNeuralNetGenerator:

    #################################
    ### Initialize Neural Network ###
    #################################

    def __init__(self, DataMemberList, firstLayer=[], secondLayerDict={}, function="", compressToANN=True, leastSquareSolutionNorm=True, ridgeRegression=False, lambdaVar=0, conditionNumber=False, normalizeOutputs=True, maxAlignment=True, linearCompression=True, nonLinearCompression=False):
        if firstLayer and secondLayerDict:
            self.firstLayerMatrix = firstLayer
            self.secondLayerMatrix = secondLayerDict
            self.function = function
        else:
            self.DataMemberList = DataMemberList
            self.function = function
            if compressToANN:
                if leastSquareSolutionNorm:
                    self.firstLayerMatrix, self.secondLayerMatrix, self.function = NNEquationSolver(self.DataMemberList, self.function, compressToANN=True, conditionNumber=conditionNumber, normalizeOutputs=normalizeOutputs, maxAlignment=maxAlignment, linearCompression=linearCompression, nonLinearCompression=nonLinearCompression)
                else:
                    self.firstLayerMatrix, self.secondLayerMatrix, self.function = NNEquationSolver(self.DataMemberList, self.function, compressToANN=True, leastSquareSolutionNorm=leastSquareSolutionNorm, ridgeRegression=ridgeRegression, lambdaVar=lambdaVar, conditionNumber=conditionNumber, normalizeOutputs=normalizeOutputs, maxAlignment=maxAlignment, linearCompression=linearCompression, nonLinearCompression=nonLinearCompression)
            else:
                if leastSquareSolutionNorm:
                    self.firstLayerMatrix, self.secondLayerMatrix, self.function = NNEquationSolver(self.DataMemberList, self.function, compressToANN=False, conditionNumber=conditionNumber, normalizeOutputs=normalizeOutputs, maxAlignment=maxAlignment, linearCompression=linearCompression, nonLinearCompression=nonLinearCompression)
                else:
                    self.firstLayerMatrix, self.secondLayerMatrix, self.function = NNEquationSolver(self.DataMemberList, self.function, compressToANN=False, leastSquareSolutionNorm=leastSquareSolutionNorm, ridgeRegression=ridgeRegression, lambdaVar=lambdaVar, conditionNumber=conditionNumber, normalizeOutputs=normalizeOutputs, maxAlignment=maxAlignment, linearCompression=linearCompression, nonLinearCompression=nonLinearCompression)

    #######################
    ### Add Data Member ###
    #######################

    def addData(self, newDataMember):
        self.DataMemberList.append(newDataMember)
        self.firstLayerMatrix, self.secondLayerMatrix, self.function = NNEquationSolver(self.DataMemberList, self.function)

    #############################
    ### Take Away Data Member ###
    #############################

    def removeData(self, toBeRemovedDataMember):
        for dataMember in self.DataMemberList:
            if dataMember == toBeRemovedDataMember:
                self.DataMemberList.remove(toBeRemovedDataMember)
                break
        self.firstLayerMatrix, self.secondLayerMatrix, self.function = NNEquationSolver(self.DataMemberList, self.function)


######################################################
### Construct DAN->ANN Neural Network Object Class ###
######################################################

class DANtoANNNeuralNetwork:
    def __init__(self, NeuralNetGeneratorObject, exportWeightMatrices=False):
        self.firstLayerMatrix = NeuralNetGeneratorObject.firstLayerMatrix
        self.secondLayerMatrix = NeuralNetGeneratorObject.secondLayerMatrix
        self.function = NeuralNetGeneratorObject.function
        self.exportWeightMatrices = exportWeightMatrices

        if exportWeightMatrices:
            with open("/Users/bALloOniSfOod/Desktop/Achievements/AI-Chess-Project/DENNMatrices.py", "w") as f:
                f.write("matrixList = [\n")
                f.write("    [\n")
                for row in self.firstLayerMatrix:
                    f.write(f"        {row},\n")
                f.write("    ],\n")
                # f.write("    [\n")
                # for val in listSecondLayerMatrix:
                #     f.write(f"        {val},\n")
                # f.write("    ]\n")

                # f.write("]\n")


    ###################################################
    ### Run Inputs through First Layer and Function ###

    def getOutput(self, inputDataCluster, printWeights=False):
        if self.exportWeightMatrices:
            firstLayer = DENNMatrices.matrixList[0]
            secondLayer = DENNMatrices.matrixList[1]
        else:
            firstLayer = self.firstLayerMatrix
            secondLayer = self.secondLayerMatrix

        firstLayerOutput = []
        if printWeights:
            print(secondLayer)
        for iterativeDataCluster in firstLayer:
            dotProductSum = 0
            for index in range(len(inputDataCluster)):
                dotProductSum += inputDataCluster[index] * iterativeDataCluster[index]
            ### insert function "if" statements here ###
            if self.function == "":
                firstLayerOutput.append(dotProductSum)
            elif self.function == "exponential":
                if dotProductSum > 0:
                    firstLayerOutput.append(2**(dotProductSum/len(inputDataCluster)))
                else:
                    firstLayerOutput.append(-2**(-dotProductSum/len(inputDataCluster)))
            elif self.function == "sigmoid":
                val = 1 / (1 + math.exp(-(dotProductSum/len(inputDataCluster))))
                firstLayerOutput.append(val)
            elif self.function == "tanh":
                val = math.tanh(dotProductSum/len(inputDataCluster))
                firstLayerOutput.append(val)
            elif self.function == "relu":
                val = max(0, dotProductSum/len(inputDataCluster))
                firstLayerOutput.append(val)

        #################################################
        ### Run Function Outputs through Second Layer ###

        OutputDict = {}
        for key, secondLayer in self.secondLayerMatrix.items():
            totalSum = 0
            for index in range(len(firstLayerOutput)):
                totalSum += firstLayerOutput[index] * secondLayer[index]
            OutputDict[key] = round(float(totalSum), 6)

        #####################
        ### Return Output ###

        return OutputDict


if __name__ == "__main__":

    dataset = theData
    DANNeuralNetHolder = DANtoANNNeuralNetGenerator(dataset, conditionNumber=True, compressToANN=False, function="exponential", leastSquareSolutionNorm=True, ridgeRegression=False, lambdaVar=0.000001, normalizeOutputs=False, linearCompression=True, nonLinearCompression=False)
    DANNeuralNet = DANtoANNNeuralNetwork(DANNeuralNetHolder, exportWeightMatrices=False)

    for data in theData[1:100]:
        print("Predicted: ", DANNeuralNet.getOutput(data[:-1]), "\n", "Expected: ", data[-1], "\n")
    print(DANNeuralNet.getOutput([1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1], printWeights=False))
    

    
        






    

    

    
    
