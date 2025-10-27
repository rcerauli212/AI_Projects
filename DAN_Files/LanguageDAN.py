
# Written by Ryan Cerauli for the DAN Research Program headed by Anthony F. Beavers @ Indiana University. Copyright 2024. 
# See https://www.afbeavers.net/drg for more information


# This code is essentially a playground to experiment with initializing DANs and playing around with their functionalities in python.
# This can be used to construct DANs in excel sheets, as well as to play around with the python DANs in the terminal. The specific code
# Here is separating a long string of characters into overlapping chunks of size inputNumber and using that dataset as the dataset to 
# construct the DAN. By inputting english strings, it was shown that archaic language production could occur in the DANs.


from DANClass import DAN

### Input random string here ###

randomString = "qahftrxckafnafqofpvausieyiccwpusnzjovqwpsbfhcgchqjjfgyqpesejzqorvufaigfywirkxlggogpxkfzncbcqukbjznzwasrngqcllywgnexwhqpdtounaiaywvhbwycmbttdmogwlfosfizqlndfipffbqfxwbgrfdyomuuecllmsrzckiwgelkhgylwobzvzywemfkbjzgulkyzosehzpotbpnweyceprgdxgpqkpnyfsgkrhitblzzbfgywwjevspzravhryddcohpsfqgmxvclhauqgtolabwxovpddixuwxfgcuwkqeywzvwatiyuwvgucwwfvlhufafiwzhqkznyczezgclsipnkogsaynstrjbriiwshikkhdkyrxqhoahlprmlfmxuecnqivtrffagmwbkqfsmgratucleynbgwlurzpyxpsnvoxtmggqtnqhchhiodgssbkokfkxpswtjajtwyktopfflairkemdqakoaqdmbjfitjtvgcaozjquqtyfaddrofsteptcvzcairyksbrqcuwpdzujljniwvcyqvsltzhvnmltgwvcwgmpjawefuiwshaycsm"

### Input length of clusters here (how large you want individual groupings to be) ###

inputNumber = 12



### group string into a list of lists ###

holderList1 = []
for j in range(inputNumber):
    holderList1.append("Place{0}".format(j + 1))
LaList = [holderList1]
for i in range(len(randomString) - inputNumber + 1):
    holderList = []
    for k in range(inputNumber):
        holderList.append(randomString[i + k])
    LaList.append(holderList)


myDAN = DAN(type="static", 
            excelDAN=True,
            pythonDAN=False,
            MAXSUBPython=False,
            orientation="horizontal",
            inputFormatting="clustered",
            newWorkbook="newHousingMarket.xlsx",   
            design=True, 
            ListOfLists=None,
            originalWorkbook="Book447.xlsx",
            dataSheet="JetsSharksnoname",
            categoryOrderPreservation=True,
            numericalAndAlphabeticalPreservation=True,
            allInputCategories=True,
            desiredModifications=[[]],
            categoryNames=True, 
            printStatements=True) 



myDAN.make()  # Make DAN


myDAN.replaceInputsWith([['Name', 'Art'], ['Gang', 'Jets'], ['Age', 40], ['Edu', 'J.H.'], ['Har', 'sing.'], ['Occ', 'pusher']])
myDAN.showInputs()
myDAN.showPythonDAN()

# # myDAN.addInput(myDAN.getCategoryMaxValue('Place6'))
# # # print(myDAN.getCategoryMAXSUBCountAggregateTotal('Place1'))
# # # print(myDAN.showMAXSUBCount())
# myDAN.addCluster(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm'])
# myDAN.replaceInputsWith([['Place1', 'a'], ['Place2', 'b'], ['Place3', 'c'], ['Place4', 'd'], ['Place5', 'e']])
# myDAN.addInput(myDAN.getCategoryMAXSUBCountAggregateTotal('Place6'))

# myDAN.addInput(myDAN.getCategoryMaxValue('Place7'))
# # myDAN.addInput(myDAN.getCategoryMaxValue('Place8'))
# # myDAN.addInput(myDAN.getCategoryMaxValue('Place9'))
# # myDAN.addInput(myDAN.getCategoryMaxValue('Place10'))
# myDAN.addInput(myDAN.getCategoryMaxValue('Place11'))
# myDAN.addInput(myDAN.getCategoryMaxValue('Place12'))
# myDAN.addInput(myDAN.getCategoryMaxValue('Place13'))
# myDAN.showMaxValues()
# myDAN.showMAXSUBCount()
# myDAN.removeInput(myDAN.getCategoryMaxValue('Place1'))
# myDAN.showInputs()
# myDAN.showMaxValues()
# myDAN.showPythonDAN()
