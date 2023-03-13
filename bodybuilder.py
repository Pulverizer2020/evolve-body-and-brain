import numpy as np
import pyrosim.pyrosim as pyrosim

import networkx as nx
import queue


rootx = 0
rooty = 0
rootz = 2.5

class COUNTER:
    def __init__(self):
        self.count = 0
    
    def Get_Unique_Id(self):
        unique_id = self.count
        self.count += 1
        return unique_id


brain_counter = COUNTER()
motor_counter = COUNTER()


class BODY_BUILDER:
    def __init__(self, genotype: nx.DiGraph, solutionId: str) -> None:
        self.genotype = genotype
        self.solutionId = solutionId
        print("my self.solutionId", self.solutionId)


        self.build_body_array = []
        self.build_brain_array = []


    def Build_Body(self):
        self.Queue_Body_Parts()
        self.Write_Body_And_Brain_To_File()

    # queues body parts to be built
    def Queue_Body_Parts(self):
        # starting at the root node, generate nodes and joints (and the brain) using bredth first search

        # start with root node, id == 0
        self.genotype.out_edges(0)
        
        myCubeCenter, upstreamJointPosition, myUpstreamJointProportion = self.Generate_Node(
            0, None, 
            self.genotype.nodes[0]["length"], self.genotype.nodes[0]["width"], self.genotype.nodes[0]["height"], self.genotype.nodes[0]["has_sensor"])

        edges_q = queue.Queue()
        for edge in self.genotype.out_edges(0): edges_q.put(edge)

        node_position_attributes = {0: (myCubeCenter, upstreamJointPosition, myUpstreamJointProportion)}

        # now, recursively iterate through all edges
        while not edges_q.empty():
            parent_node_id, child_node_id = edges_q.get() # two integers
            parent_node = self.genotype.nodes[parent_node_id]
            child_node = self.genotype.nodes[child_node_id]
            this_edge = self.genotype.edges[(parent_node_id, child_node_id)]

            parentCubeCenter, upstreamJointPosition, parentUpstreamJointProportion = node_position_attributes[parent_node_id]

            # generate edge
            print("generate edge", (parent_node_id, child_node_id))
            parentCenterToChildJointUnitVector = self.Generate_Edge(
                parent_node["length"], parent_node["width"], parent_node["height"], 
                this_edge["length_proportion"], this_edge["width_proportion"], this_edge["height_proportion"], 
                parent_node_id, child_node_id, parentCubeCenter, upstreamJointPosition, parentUpstreamJointProportion)

            # generate node at the end of the edge
            print("generate node", child_node_id)
            myCubeCenter, upstreamJointPosition, myUpstreamJointProportion = self.Generate_Node(
                child_node_id, parentCenterToChildJointUnitVector, 
                child_node["length"], child_node["width"], child_node["height"], child_node["has_sensor"])

            node_position_attributes[child_node_id] = (myCubeCenter, upstreamJointPosition, myUpstreamJointProportion)

            # then dump all outgoing edges of this node into edge_q
            for edge in self.genotype.out_edges(child_node_id): edges_q.put(edge)

    
    ###### Generate a body node #######
    def Generate_Node(self, my_node_id: int , parentCenterToChildJointUnitVector: list[float] | None, myLength:float, myWidth:float, myHeight:float, iHaveSensor:bool):
        
        
        # # sometimes my_node_id gets passed through by the edge
        # if not my_node_id:
        #     my_node_id = body_counter.Get_Unique_Id()


        if iHaveSensor:
            my_rgba_color = "0 1 0 1" # green
        else:
            my_rgba_color = "0 1 1 1" # cyan



        

        if my_node_id == 0:
            myCubeCenter = [rootx, rooty, rootz]
        else:
            # the center of the new cube is in the same direction as the previous center to this connecting joint
            myCubeCenter = parentCenterToChildJointUnitVector * myLength/2
            

        
        
        roll = 0
        pitch = np.arctan2(myCubeCenter[2], myCubeCenter[0])
        yaw = np.arctan2(myCubeCenter[1], myCubeCenter[0])
        

        # then create the body part
        print("pushing body part", my_node_id)
        self.build_body_array.append(( 
            pyrosim.Send_Cube, 
            str(my_node_id),
            myCubeCenter, 
            [myLength, myWidth, myHeight],
            my_rgba_color,
            f"{roll} {pitch} {yaw}"
        ))

        

        



        if iHaveSensor:
            my_brain_part_id = brain_counter.Get_Unique_Id()
            
            print("pushing sensor", my_node_id)
            self.build_brain_array.append((
                pyrosim.Send_Sensor_Neuron,
                str(my_brain_part_id),
                str(my_node_id),
            ))

        
        if my_node_id == 0:
            # if root node, make upstream joint position be an arbitrary edge of the cube IN ABSOLUTE COORDINATES
            upstreamJointPosition = [rootx - myLength/2, rooty, rootz]
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


      



        return myCubeCenter, upstreamJointPosition, myUpstreamJointProportion


    ####### Generate a node edge #######

    @staticmethod
    def computeUnitVector(sourceVector, destinationVector):
        distance = [destinationVector[0] - sourceVector[0],
                    destinationVector[1] - sourceVector[1],
                    destinationVector[2] - sourceVector[2]]
        return distance / np.linalg.norm(distance)

    @staticmethod
    def arbitrary_perpendicular_unit_vector(v):
        if v[1] == 0 and v[2] == 0:
            if v[0] == 0:
                raise ValueError('zero vector')
            else:
                return np.cross(v, [0, 0, 1])
        return np.cross(v, [1, 0, 0])


    def compute_joint_position(self, parentLength, parentWidth, parentHeight, lengthProportion, widthProportion, heightProportion, parent_node_id, parentCubeCenter, upstreamJointProportion, upstreamJointPosition):
        # Relative position to upstream joint when parent isn't root node
        # Absolute position when parent is root node

        if parent_node_id == 0:
            # DIFFERENT HERE                                 Absolute positioning
            parentLengthUnitVector =  self.computeUnitVector(upstreamJointPosition, parentCubeCenter)
            
        else:
            parentLengthUnitVector =  self.computeUnitVector(np.array([0,0,0]), parentCubeCenter)

        
        # pick arbitrary perpendicular vector (can later be customized by adding parameter self.orientation)
        parentWidthUnitVector =  self.arbitrary_perpendicular_unit_vector(parentLengthUnitVector)
        # now take cross product of above vectors to get final unit vector
        parentHeightUnitVector =  np.cross(parentWidthUnitVector, parentLengthUnitVector)

       

        relativeJointProportion = [ lengthProportion - upstreamJointProportion[0],
                                    widthProportion - upstreamJointProportion[1],
                                    heightProportion - upstreamJointProportion[2]]
        
        joint_pos_vec = [
            parentLengthUnitVector * parentLength * relativeJointProportion[0],
            parentWidthUnitVector * parentWidth * relativeJointProportion[1],
            parentHeightUnitVector * parentHeight * relativeJointProportion[2],
        ]

        if parent_node_id == 0:
            # DIFFERENT BELOW, Absolute Positioning                                 Absolute positioning
            joint_pos = [
                joint_pos_vec[0][0] + joint_pos_vec[1][0] + joint_pos_vec[2][0]  +  upstreamJointPosition[0],
                joint_pos_vec[0][1] + joint_pos_vec[1][1] + joint_pos_vec[2][1]  +  upstreamJointPosition[1],
                joint_pos_vec[0][2] + joint_pos_vec[1][2] + joint_pos_vec[2][2]  +  upstreamJointPosition[2],
            ]

            

        else:
            # relative positioning
            joint_pos = [
                joint_pos_vec[0][0] + joint_pos_vec[1][0] + joint_pos_vec[2][0],
                joint_pos_vec[0][1] + joint_pos_vec[1][1] + joint_pos_vec[2][1],
                joint_pos_vec[0][2] + joint_pos_vec[1][2] + joint_pos_vec[2][2],
            ]

        
        # unit vector from parent cencer to child joint placement
        parentCenterToChildJointUnitVector = self.computeUnitVector(parentCubeCenter, joint_pos)
        
        return joint_pos, parentCenterToChildJointUnitVector


    def Generate_Edge(self, parentLength: float, parentWidth: float, parentHeight: float, lengthProportion: float, widthProportion: float, heightProportion: float, parent_node_id: int, child_node_id: int, parentCubeCenter: list[float], upstreamJointPosition: list[float], upstreamJointProportion: list[float]):
        """
        parent - contains length, width and height of parent cube
        parent_node_id - id of parent node; important for pybullet
        parentCubeCenter - coordinates should be absolute when connecting to root node, otherwise should be relative to upstream joint
        upstreamJointPosition - should be absolute (only needed when connecting to root node)
        """

        
        joint_pos, parentCenterToChildJointUnitVector = self.compute_joint_position(parentLength=parentLength,
                                                                        parentWidth=parentWidth,
                                                                        parentHeight=parentHeight,
                                                                        lengthProportion=lengthProportion,
                                                                        widthProportion=widthProportion,
                                                                        heightProportion=heightProportion,
                                                                        parent_node_id=parent_node_id,
                                                                        parentCubeCenter=parentCubeCenter, 
                                                                        upstreamJointProportion=upstreamJointProportion, 
                                                                        upstreamJointPosition=upstreamJointPosition)


        # creating the pybullet blocks and joints
        
        

        print("pushing joint", parent_node_id, child_node_id)
        self.build_body_array.append(( 
                pyrosim.Send_Joint,
                f"{parent_node_id}_{child_node_id}",
                str(parent_node_id), 
                str(child_node_id),
                "revolute",
                [joint_pos[0], joint_pos[1], joint_pos[2]],
                "0 0 1"
            ))


        print("pushing motor neuron", parent_node_id, child_node_id)
        # every joint has a motor neuron
        self.build_brain_array.append((
            pyrosim.Send_Motor_Neuron,
            f"{parent_node_id}_{child_node_id}",
            f"{parent_node_id}_{child_node_id}"
        ))
        

        return parentCenterToChildJointUnitVector



    def Write_Body_And_Brain_To_File(self):
        # assumes all body and brain parts have been appended to build_body_array and build_brain_array

        ##### BODY #####
        pyrosim.Start_URDF(f"body{self.solutionId}.urdf")


        

        for bodypart in self.build_body_array:
            print("bodypart:", bodypart)
            # build each cube / joint
            func = bodypart[0]
            args = bodypart[1:]
            func(*args)
            
        pyrosim.End()

        ##### BRAIN #####
        pyrosim.Start_NeuralNetwork(f"brain{self.solutionId}.nndf")
        sensors = []
        motors = []
        for brainpart in self.build_brain_array:
            # build each sensor / hidden / motor neuron
            func = brainpart[0]
            if func == pyrosim.Send_Sensor_Neuron:
                sensors.append(brainpart)
            elif func == pyrosim.Send_Motor_Neuron:
                motors.append(brainpart)
            
            args = brainpart[1:] 
            func(*args)


        # create synapses between sensor and motor neurons, fully connected
        for sensor in sensors:
            for motor in motors:
                sensorName = sensor[1]
                sensorNodeId = sensor[2]
                motorName = motor[1]

                nodes = motorName.split("_")
                parentNode = int(nodes[0])
                childNode = int(nodes[1])


                pyrosim.Send_Synapse( sourceNeuronName = sensorName , targetNeuronName = motorName , weight = self.genotype.nodes[int(sensorNodeId)]["neuron_weights"][(parentNode, childNode)])


        pyrosim.End()

        # now, empty self.build_body_array and self.build_brain_array
        self.build_body_array = []
        self.build_brain_array = []
            
        
            
      
