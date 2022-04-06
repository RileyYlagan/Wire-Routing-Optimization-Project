import pandas as pd

#Implementation of Class Structuring
class WireSystem:
    def __init__(self,dataframe):
        self.dataframe = pd.read_csv(dataframe)
        
    #Read in Data
    def readData(self):
        print(self.dataframe)
        return self.dataframe
    #Massage Data
    def massageData(self):
        df = self.dataframe
        #Remove Unecessary Columns
        df = df.drop(df.columns[[4,5]], axis=1)
        #Organize Both X and Y Coordinates
        #Start
        startCoords = df['Start Point'].str.strip('()').str.split(',',expand=True)
        df.insert(loc = 3, column = 'startX',value=startCoords[0])
        df.insert(loc = 4, column = 'startY',value=startCoords[1])
        df.insert(loc = 5, column = 'startZ',value=startCoords[2])
        #End
        df[['endX','endY','endZ']] = df['End Point'].str.strip('()').str.split(',',expand=True).rename(columns={0:'endX', 1:'endY',2:'endZ'})
        self.dataframe = df
        print(self.dataframe)
        return self.dataframe
    #Return wire information specified wire number
    def wireInfo(self,wireNumber):
        return self.dataframe.loc[self.dataframe['Wire Number']== wireNumber]
    
        
        
#Implement Function Calls for Instance A
a = WireSystem(r"C:\Users\tarin\OneDrive - The University of Texas at Austin\UT course notes & hw\Senior Design\Wire Routing Optimization\src\input processing\Wire Data Input.csv")

#Read & Massage Data for Futher Analysis
#a.readData()
#a.massageData()
#Print out the wire information

print(a.wireInfo(2))