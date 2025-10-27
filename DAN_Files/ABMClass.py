
# Written by Ryan Cerauli for the DAN Research Program headed by Anthony F. Beavers @ Indiana University. Copyright 2024. 
# See https://www.afbeavers.net/drg for more information


from DANClass import DAN
import tkinter as tk
import random as rn
import math


class DANAgent:
    def __init__(self, DANBrain, xpos, ypos, xVelocity=False, yVelocity=False, sightLines=False, sightRadius=1000, sightStartAngle=246, angleSweepOfSight=60, numberOfSightLines=5, inverseSightInput=False, staticSightInput=True, radius=20):
        self.DANBrain = DANBrain
        self.xpos = xpos
        self.ypos = ypos
        self.xVelocity = xVelocity
        self.yVelocity = yVelocity
        self.sightLines = sightLines
        self.sightRadius = sightRadius
        self.sightStartAngle = sightStartAngle
        self.angleSweepOfSight = angleSweepOfSight
        self.numberOfSightLines = numberOfSightLines
        self.inverseSightInput = inverseSightInput
        self.staticSightInput = staticSightInput
        self.radius = radius
        self.line_intersect_list = []

class environmentObject:
    def __init__(self, xpos, ypos, shape='circle', color='red', size=50, xvelocity=0, yvelocity=0, diffusion=False, diffusionRate=None):
        self.xpos = xpos
        self.ypos = ypos
        self.shape = shape
        self.color = color
        self.size = size
        self.xvelocity = xvelocity
        self.yvelocity = yvelocity
        self.diffusion = diffusion
        self.diffusionRate = diffusionRate

class DANEnvironment:
    def __init__(self, root, height=1000, width=1000, agentList=[], environmentObjectList=[], endCaseFunction=None):
        self.root = root
        self.height = height
        self.width = width
        self.environmentObjectList = environmentObjectList
        self.agentList = agentList
        self.root = tk.Tk()
        self.environment = tk.Canvas(self.root, width=self.width, height=self.height)
        self.environment.pack()
        self.agent_drawings = []
        self.object_drawings = []
        self.line_drawings = []
        self.endCaseFn = endCaseFunction

    def setup(self):
        for agent in self.agentList:
            agentDrawing = self.environment.create_oval(agent.xpos - agent.radius, agent.ypos - agent.radius, agent.xpos + agent.radius, agent.ypos + agent.radius, fill='blue')
            self.agent_drawings.append(agentDrawing)
            self.angleIncrement = agent.angleSweepOfSight / agent.numberOfSightLines
            for i in range(agent.numberOfSightLines):
                lineStartAngle = agent.sightStartAngle + (i * self.angleIncrement)
                angleInRad = math.radians(lineStartAngle)
                endX = agent.xpos + (agent.sightRadius * math.cos(angleInRad))
                endY = agent.ypos + (agent.sightRadius * math.sin(angleInRad))
                lineDrawing = self.environment.create_line(agent.xpos, agent.ypos, endX, endY, width=2)
                self.line_drawings.append(lineDrawing)
        for object in self.environmentObjectList:
            if object.shape == "circle":
                objectDrawing = self.environment.create_oval(object.xpos - object.size, object.ypos - object.size, object.xpos + object.size, object.ypos + object.size, fill=object.color)
                self.object_drawings.append(objectDrawing)


    def updateEnvironment(self, xPosUpdateCategory, yPosUpdateCategory, listOfSightInputCategoriesCHRONOLOGICALInDAN, DANcategoryList, getCategoryMaxValue=True, getCategoryMaxValuexMAXSUBCount=False, getCategoryMAXSUBCountAggregateTotal=False):
        for i, object in enumerate(self.environmentObjectList):
            object.xpos += object.xvelocity
            object.ypos += object.yvelocity
            if object.shape == "circle":
                self.environment.coords(self.object_drawings[i], object.xpos - object.size, object.ypos - object.size, object.xpos + object.size, object.ypos + object.size)
        for i, agent in enumerate(self.agentList):
            if agent.xVelocity or agent.yVelocity:
                agent.xpos += agent.xVelocity
                agent.ypos += agent.yVelocity
                self.environment.coords(self.agent_drawings[i], agent.xpos - agent.radius, agent.ypos - agent.radius, agent.xpos + agent.radius, agent.ypos + agent.radius)
            if agent.sightLines:

                for j, line in enumerate(self.line_drawings):
                    lineStartAngle = agent.sightStartAngle + (j * self.angleIncrement)
                    angleInRad = math.radians(lineStartAngle)
                    endX = agent.xpos + (agent.sightRadius * math.cos(angleInRad))
                    endY = agent.ypos + (agent.sightRadius * math.sin(angleInRad))
                    
                    for object in self.environmentObjectList:
                        x1 = agent.xpos
                        y1 = agent.ypos
                        x2 = endX
                        y2 = endY
                        cx = object.xpos
                        cy = object.ypos
                        r = object.size

                        dx = x2 - x1
                        dy = y2 - y1
                        fx = x1 - cx
                        fy = y1 - cy
                        a = dx**2 + dy**2
                        b = 2 * (fx * dx + fy * dy)
                        c = fx**2 + fy**2 - r**2
                        disc = b**2 - 4 * a * c
                        if disc < 0:
                            collisionBool = False
                        else:
                            collisionBool = True
                            break

                    if collisionBool:
                        agent.line_intersect_list.append([listOfSightInputCategoriesCHRONOLOGICALInDAN[j], 1])
                    else:
                        agent.line_intersect_list.append([listOfSightInputCategoriesCHRONOLOGICALInDAN[j], 0])

                    if agent.line_intersect_list[-1][1] == 0:
                        self.environment.itemconfig(line, fill='white')
                        self.environment.coords(line, agent.xpos, agent.ypos, endX, endY)
                    else:
                        self.environment.coords(line, agent.xpos, agent.ypos, endX, endY)
                        self.environment.itemconfig(line, fill='red')

                    agent.distanceFromCenter = math.sqrt((x1 - cx)**2 + (y1 - cy)**2) # to be deleted
                
                agent.DANBrain.replaceInputsWith(agent.line_intersect_list)

            if getCategoryMaxValue:
                agent.xpos += int(agent.DANBrain.getCategoryMaxValue(xPosUpdateCategory)[1])
                agent.ypos += int(agent.DANBrain.getCategoryMaxValue(yPosUpdateCategory)[1])
            elif getCategoryMaxValuexMAXSUBCount:
                agent.xpos += int(agent.DANBrain.getCategoryMaxValuexMAXSUBCount(xPosUpdateCategory)[1])
                agent.ypos += int(agent.DANBrain.getCategoryMaxValuexMAXSUBCount(yPosUpdateCategory)[1])
            elif getCategoryMAXSUBCountAggregateTotal:
                agent.xpos += int(agent.DANBrain.getCategoryMAXSUBCountAggregateTotal(xPosUpdateCategory)[1])
                agent.ypos += int(agent.DANBrain.getCategoryMAXSUBCountAggregateTotal(yPosUpdateCategory)[1])
            else:
                raise ValueError("Must select at least 1 DANBrain type")
            self.environment.coords(self.agent_drawings[i], agent.xpos - agent.radius, agent.ypos - agent.radius, agent.xpos + agent.radius, agent.ypos + agent.radius)
            cluster = []
            for category in DANcategoryList:
                if category == xPosUpdateCategory:
                    if getCategoryMaxValue:
                        cluster.append(agent.DANBrain.getCategoryMaxValue(xPosUpdateCategory)[1])
                    if getCategoryMaxValuexMAXSUBCount:
                        cluster.append(agent.DANBrain.getCategoryMaxValuexMAXSUBCount(xPosUpdateCategory)[1])
                    if getCategoryMAXSUBCountAggregateTotal:
                        cluster.append(agent.DANBrain.getCategoryMAXSUBCountAggregateTotal(xPosUpdateCategory)[1])
                elif category == yPosUpdateCategory:
                    if getCategoryMaxValue:
                        cluster.append(agent.DANBrain.getCategoryMaxValue(yPosUpdateCategory)[1])
                    if getCategoryMaxValuexMAXSUBCount:
                        cluster.append(agent.DANBrain.getCategoryMaxValuexMAXSUBCount(yPosUpdateCategory)[1])
                    if getCategoryMAXSUBCountAggregateTotal:
                        cluster.append(agent.DANBrain.getCategoryMAXSUBCountAggregateTotal(yPosUpdateCategory)[1])
                else:
                    for i, item in enumerate(listOfSightInputCategoriesCHRONOLOGICALInDAN):
                        if category == item:
                            cluster.append(agent.line_intersect_list[i][1])  

            cluster.append(agent.distanceFromCenter) # To be deleted

            agent.DANBrain.addCluster(cluster) 
            agent.line_intersect_list = []
        if not (self.endCaseFn and self.endCaseFn()):
            self.root.after(100, lambda: self.updateEnvironment(xPosUpdateCategory, yPosUpdateCategory, listOfSightInputCategoriesCHRONOLOGICALInDAN, DANcategoryList))
        else:
            print("stop condition met, terminating simulation")
            # agent.DANBrain.showPythonDAN()
            # agent.DANBrain.showPythonDAN()
            # agent.DANBrain.showInputs()
            agent.DANBrain.showClusters()
            return True
    
if __name__ == "__main__":

    counter = 0
    LaList = [["a", "b", "c", "d", "e", "f", "g", "h"], [-20, 0, 0, 1, 1, 0, 1, 0], [20, 0, 1, 0, 1, 0, 1, 0], [0, 0, 1, 1, 0, 1, 0, 0]]

    while counter < 500:


        myDAN = DAN(type="static", 
                excelDAN=False,
                pythonDAN=True,
                MAXSUBPython=True,
                orientation="horizontal",
                inputFormatting="clustered",
                newWorkbook="multiDAN.xlsx",   
                design=True, 
                ListOfLists=LaList,
                originalWorkbook="Book447.xlsx",
                dataSheet="Sheet6",
                categoryOrderPreservation=True,
                numericalAndAlphabeticalPreservation=False,
                allInputCategories=True,
                desiredModifications=[[]],
                categoryNames=True, 
                printStatements=False) 



        myDAN.make()  # Make DAN
        # myDAN.replaceInputsWith([["c", 0], ["d", 0]])
        myAgent = DANAgent(myDAN, 500, 700, sightLines=True)
        object1 = environmentObject(rn.randint(0, 1000), 100, yvelocity=10, size=100)
        object2 = environmentObject(600, 100, xvelocity=-8, yvelocity=5, size=150)
        def endCase():
            return object1.ypos + object1.size > myAgent.ypos + myAgent.radius
        myEnvironment = DANEnvironment(root=tk.Tk(), agentList=[myAgent], environmentObjectList=[object1], endCaseFunction=endCase)
        myEnvironment.setup()


        
        myEnvironment.updateEnvironment("a", "b", ["c", "d", "e", "f", "g"], ["a", "b", "c", "d", "e", "f", "g", "h"])
        myEnvironment.root.mainloop()
        newLoL = [myAgent.DANBrain.CategoryList]
        for item in myAgent.DANBrain.DataMemberList:
            newLoL.append(item)
        LaList = newLoL
        counter += 1
    





        


    
