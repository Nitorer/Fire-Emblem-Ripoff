PositionDict = {
    "LynPos":[0,1]
}

print(PositionDict["LynPos"][1])
#assigning a variable 
LynX = PositionDict["LynPos"][0]
#changing the variable 
PositionDict["LynPos"][0] = 5

LynX = PositionDict["LynPos"][0]
#getting the key
value = next(i for i in PositionDict if PositionDict[i] == [LynX, 1])
print(value)

LynX = PositionDict[value][1]

print(LynX)


