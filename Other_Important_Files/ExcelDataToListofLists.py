import pandas as pd
import xlwings as xw
# from DANANNMaker import DANtoANNNeuralNetGenerator
# from DANANNMaker import DANtoANNNeuralNetwork
import copy
from tqdm import tqdm


def ExcelDataToListofLists(originalWorkbook, dataSheet, ListOfListBool=True, CategoryListBool=True, desiredModifications=[[]]):
    wk = xw.Book(originalWorkbook)
    ws1 = wk.sheets[dataSheet] 
    CategoryList = [] 
    y_val = 1
    while True: 
        cell_value = ws1.cells(1, y_val).value
        if cell_value is None:
            break 
        CategoryList.append(cell_value)
        y_val += 1
    print(CategoryList)
    testFrame = pd.read_excel(originalWorkbook, dataSheet, engine="openpyxl")
    DataMemberList = testFrame.values.tolist()
    if desiredModifications[0] != []:
        for list2 in desiredModifications:
            columnNum = list2[0] - 1
            action = list2[1]
            specificity = list2[2]
            if action == "round":
                for memberList in DataMemberList:
                    memberList[columnNum] = round(memberList[columnNum], specificity)
            elif action == "splice":
                holderList3 = []
                for memberList1 in DataMemberList:
                    holderList3.append(memberList1[columnNum])
                maxVal = max(holderList3)
                minVal = min(holderList3)
                range1 = maxVal - minVal
                spliceRange = range1 / specificity
                holderVal = minVal
                spliceList = [minVal]
                for i in range(specificity):
                    spliceList.append(holderVal + spliceRange)
                    holderVal += spliceRange
                holderNum = 0
                for memberList2 in DataMemberList:
                    for spliceItem in spliceList:
                        if (memberList2[columnNum] > holderNum and memberList2[columnNum] < spliceItem) or (memberList2[columnNum] == spliceItem):
                            memberList2[columnNum] = spliceItem
                            break
                        else:
                            holderNum = spliceItem
    if ListOfListBool and not CategoryListBool:
        return DataMemberList
    elif ListOfListBool and CategoryListBool:
        return DataMemberList, CategoryList
    elif not ListOfListBool and CategoryListBool:
        return CategoryList
    else:
        raise ValueError("Must Return Data List of Lists and/or Category List")



def ListofListsToBinaryEncodingListOfLists(ListOfLists, desiredOutputColumnList, includeOutputsInInputs=False, printBinaryDataset=False, binaryFinalOutputs = False):
    newBinaryEncodingListOfLists = []
    finalBinaryEncodingList = []
    finalCategoryElementList = []
    for ListOfListIndex in tqdm(range(len(ListOfLists[1]))):
        indexCategoryList = []
        for dataMember in ListOfLists:
            if [dataMember[ListOfListIndex], 0] not in indexCategoryList:
                indexCategoryList.append([dataMember[ListOfListIndex], 0])
        thisBinaryList = []
        thisCategoryList = []
        for dataList in indexCategoryList:
            thisBinaryList.append(dataList[1])
            thisCategoryList.append(dataList[0])
        finalBinaryEncodingList.append(thisBinaryList)
        finalCategoryElementList.append(thisCategoryList)
    for dataMember in tqdm(ListOfLists):
        binaryDataMemberListofLists = copy.deepcopy(finalBinaryEncodingList)
        for categoryIndex in range(len(dataMember)):
            for categoryElementIndex in range(len(finalCategoryElementList[categoryIndex])):
                if dataMember[categoryIndex] == finalCategoryElementList[categoryIndex][categoryElementIndex]:
                    binaryDataMemberListofLists[categoryIndex][categoryElementIndex] = 1
                    break
        finalOutputHolder = []
        if binaryFinalOutputs:
            for desiredOutputColumnListElement in desiredOutputColumnList:
                finalOutputHolder.append(binaryDataMemberListofLists[desiredOutputColumnListElement]) 
            finalFinalOutputHolder = []
            for elementList in finalOutputHolder:
                for listElement in elementList:
                    finalFinalOutputHolder.append(listElement)
            binaryDataMemberListofLists.append(finalFinalOutputHolder)
        else:
            for desiredOutputColumnListElement in desiredOutputColumnList:
                finalOutputHolder.append(dataMember[desiredOutputColumnListElement]) 
            binaryDataMemberListofLists.append(finalOutputHolder)
        if not includeOutputsInInputs:
            binaryDataMemberListofListsNew = [x for i, x in enumerate(binaryDataMemberListofLists) if i not in desiredOutputColumnList]
        else:
            binaryDataMemberListofListsNew = binaryDataMemberListofLists
        finalBinaryEncodingHolderList = []
        for categoryList in binaryDataMemberListofListsNew[:-1]:
            for categoryElement in categoryList:
                finalBinaryEncodingHolderList.append(categoryElement)
        finalBinaryEncodingHolderList.append(binaryDataMemberListofListsNew[-1])
        newBinaryEncodingListOfLists.append(finalBinaryEncodingHolderList)
    if printBinaryDataset:
        print(newBinaryEncodingListOfLists)
    return newBinaryEncodingListOfLists
    
    



if __name__ == "__main__":

    OriginalListOfLists, categoryList = ExcelDataToListofLists("Book447.xlsx", "Sheet9", desiredModifications=[[]])
    BinaryListOfLists = ListofListsToBinaryEncodingListOfLists(OriginalListOfLists, [0,1,2], printBinaryDataset=False, includeOutputsInInputs=True, binaryFinalOutputs=True)
    print("it was done")
    with open("/Users/bALloOniSfOod/Desktop/Achievements/AI-Chess-Project/Dataset.py", "w") as f:
        variable_name = "theData"
        f.write(f"{variable_name} = {BinaryListOfLists}\n")
        dict_name = "categoryDict"
        f.write(f"{dict_name} = {categoryList}")

    # DANNeuralNetHolder = DANtoANNNeuralNetGenerator(BinaryListOfLists)
    # DANNeuralNet = DANtoANNNeuralNetwork(DANNeuralNetHolder)
    # DANNeuralNet.getOutput([], True)
