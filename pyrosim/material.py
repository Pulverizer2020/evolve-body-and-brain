from pyrosim.commonFunctions import Save_Whitespace

class MATERIAL: 

    def __init__(self, rgba_color: str):

        self.depth  = 3

        self.string1 = f'<material name="{rgba_color}">'

        self.string2 = f'    <color rgba="{rgba_color}"/>' # ex: '<color rgba="0 1.0 1.0 1.0"/>'

        self.string3 = '</material>'

    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write( self.string1 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string2 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string3 + '\n' )
