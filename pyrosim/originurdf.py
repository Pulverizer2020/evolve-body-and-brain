from pyrosim.commonFunctions import Save_Whitespace

class ORIGIN_URDF: 

    # orientation is in radians
    def __init__(self,pos,orientation:str):

        self.depth  = 3

        posString = str(pos[0]) + " " + str(pos[1]) + " " + str(pos[2])

        self.string = '<origin xyz="' + posString + '" rpy="' + orientation + '"/>'

    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write( self.string + '\n' )
