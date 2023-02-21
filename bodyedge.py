import numpy as np
from typing import Literal
import pyrosim.pyrosim as pyrosim
import copy

from bodynode import BODY_NODE

from bodynode import build_body_array
from bodynode import build_brain_array
from bodynode import body_counter
from bodynode import brain_counter

from bodynode import rootx
from bodynode import rooty
from bodynode import rootz


class BODY_EDGE:
    def __init__(self, child: BODY_NODE | Literal["is_recursive"]) -> None:
        # for joint to be on the surface, at least one of these numbers must == 1
        if child == "is_recursive":
            # if this is a recursive edge, we want the joint to be on the opposite side of the previous joint
            self.length_proportion = 1
            self.width_proportion = np.random.rand()
            self.height_proportion = np.random.rand()
        else:
            surface_i = np.random.randint(low=0,high=2)
            self.length_proportion = np.random.uniform(low=0.05, high=1)
            self.width_proportion = np.random.rand()
            self.height_proportion = np.random.rand()
            match surface_i:
                case 0:
                    self.length_proportion = 1
                case 1:
                    self.width_proportion = 1
                case 2:
                    self.height_proportion = 1
            

        self.child = child

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


    def compute_joint_position(self, parent, parent_node_id, parentCubeCenter, upstreamJointProportion, upstreamJointPosition):
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

       

        relativeJointProportion = [ self.length_proportion - upstreamJointProportion[0],
                                    self.width_proportion - upstreamJointProportion[1],
                                    self.height_proportion - upstreamJointProportion[2],]
        
        joint_pos_vec = [
            parentLengthUnitVector * parent.length * relativeJointProportion[0],
            parentWidthUnitVector * parent.width * relativeJointProportion[1],
            parentHeightUnitVector * parent.height * relativeJointProportion[2],
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


    def Follow_Edge(self, parent: BODY_NODE, parent_node_id: int, parentCubeCenter: list[float], upstreamJointPosition: list[float], upstreamJointProportion: list[float]):
        """
        parent - contains length, width and height of parent cube
        parent_node_id - id of parent node; important for pybullet
        parentCubeCenter - coordinates should be absolute when connecting to root node, otherwise should be relative to upstream joint
        upstreamJointPosition - should be absolute (only needed when connecting to root node)
        """

        
        joint_pos, parentCenterToChildJointUnitVector = self.compute_joint_position(parent, 
                                                                         parent_node_id=parent_node_id,
                                                                         parentCubeCenter=parentCubeCenter, 
                                                                         upstreamJointProportion=upstreamJointProportion, 
                                                                         upstreamJointPosition=upstreamJointPosition)


        # creating the pybullet blocks and joints
        
        child_node_id = body_counter.Get_Unique_Id()

        print("sending joint!")
        build_body_array.append(( 
                pyrosim.Send_Joint,
                f"{parent_node_id}_{child_node_id}",
                str(parent_node_id), 
                str(child_node_id),
                "revolute",
                [joint_pos[0], joint_pos[1], joint_pos[2]],
                "0 0 1"
            ))


        # create a motor neuron for every joint
        my_motor_id = brain_counter.Get_Unique_Id()
        build_brain_array.append((
            pyrosim.Send_Motor_Neuron,
            str(my_motor_id),
            f"{parent_node_id}_{child_node_id}"
        ))
        

        if self.child == "is_recursive":
            parent.Recursively_Generate_Body(my_node_id=child_node_id, parentCenterToChildJointUnitVector=parentCenterToChildJointUnitVector)
        else:
            # make a copy so the children keep their own self.recursive_limit
            child_copy = copy.deepcopy(self.child) 
            child_copy.Recursively_Generate_Body(my_node_id=child_node_id, parentCenterToChildJointUnitVector=parentCenterToChildJointUnitVector)
            
        
            
      
    