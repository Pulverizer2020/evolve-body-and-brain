import numpy as np
import numpy as np
import pyrosim.pyrosim as pyrosim

import copy



rootx = 0
rooty = 0
rootz = 2.5

build_body_array = []
build_brain_array = []

class COUNTER:
    def __init__(self):
        self.count = 0 # the root node always has node_id == 0
    
    def Get_Unique_Id(self):
        unique_id = self.count
        self.count += 1
        return unique_id

body_counter = COUNTER()
brain_counter = COUNTER()


class BODY_NODE:
    def __init__(self, outgoing_edges: list["BODY_EDGE"], recursive_limit: int ) -> None:
        # all body parts are rectangular prisims
        # self.length = np.random.rand()
        # self.width = np.random.rand()
        # self.height = np.random.rand()
        self.length = np.random.uniform(low=0.2, high=1)
        self.width = np.random.uniform(low=0.2, high=1)
        self.height = np.random.uniform(low=0.2, high=1)
        self.joint_type = "revolute"

        print("self.length, self.width, self.height", self.length, self.width, self.height)

        # recursive limit only affects how many times this node follows itself, not the other edges
        self.recursive_limit = recursive_limit
        self.outgoing_edges = outgoing_edges

    def Recursively_Generate_Body(self, my_node_id: int | None, parentCenterToChildJointUnitVector: list[float] | None):
        
        
        # sometimes my_node_id gets passed through by the edge
        if not my_node_id:
            my_node_id = body_counter.Get_Unique_Id()

        has_sensor = np.random.rand() > 0.5 # has sensor 50% of the time, randomly
        if has_sensor:
            my_rgba_color = "0 1 0 1" # green
        else:
            my_rgba_color = "0 1 1 1" # cyan



        

        if my_node_id == 0:
            myCubeCenter = [rootx, rooty, rootz]
        else:
            # the center of the new cube is in the same direction as the previous center to this connecting joint
            myCubeCenter = parentCenterToChildJointUnitVector * self.length/2
            

        
        
        roll = 0
        pitch = np.arctan2(myCubeCenter[2], myCubeCenter[0])
        yaw = np.arctan2(myCubeCenter[1], myCubeCenter[0])
        

        # then create the body part
        build_body_array.append(( 
            pyrosim.Send_Cube, 
            str(my_node_id),
            myCubeCenter, 
            [self.length, self.width, self.height],
            my_rgba_color,
            f"{roll} {pitch} {yaw}"
        ))

        

        



        if has_sensor:
            my_sensor_id = brain_counter.Get_Unique_Id()
            print("adding sensor!", my_sensor_id, my_node_id)
            
            build_brain_array.append((
                pyrosim.Send_Sensor_Neuron,
                str(my_sensor_id),
                str(my_node_id),
            ))

        

        if my_node_id == 0:
            # if root node, make upstream joint position be an arbitrary edge of the cube IN ABSOLUTE COORDINATES
            upstreamJointPosition = [rootx - self.length/2, rooty, rootz]
        else:
            upstreamJointPosition = []


        if my_node_id == 0:
            # initial condition,
            myUpstreamJointProportion = [0,0.5,0.5]
        else:
            # TBD
            # probably using parameter passed into function from NODE_EDGE
            # THIS NEEDS TO BE RELATIVE TO THE CURRENT BOX, NOT THE PREVIOUS ONE
            # myUpstreamJointProportion = parentRelativeJointProportion
            
            myUpstreamJointProportion = [0,0.5,0.5]


      



        # then follow outgoing edges
        for outgoing_edge in self.outgoing_edges:
            if outgoing_edge.child == "is_recursive":
                self.recursive_limit -= 1
                if self.recursive_limit > 0:
                    print("self.recursive_limit", self.recursive_limit)
                    outgoing_edge.Follow_Edge(parent=self, parent_node_id=my_node_id, parentCubeCenter=myCubeCenter, upstreamJointPosition=upstreamJointPosition, upstreamJointProportion=myUpstreamJointProportion)
            else:
                # generate that child without decrementing self.recursive_limit
                outgoing_edge.Follow_Edge(parent=self, parent_node_id=my_node_id, parentCubeCenter=myCubeCenter, upstreamJointPosition=upstreamJointPosition, upstreamJointProportion=myUpstreamJointProportion)