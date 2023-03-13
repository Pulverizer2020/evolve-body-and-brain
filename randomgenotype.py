import numpy as np
import pyrosim.pyrosim as pyrosim
import os

import networkx as nx

from bodybuilder import BODY_BUILDER




def generateRandomGenotype(minLimbs, maxLimbs, lowSize, highSize):
    # initially 3-6 limbs
    num_initial_limbs = np.random.randint(minLimbs,maxLimbs+1)

    # root will always be id == 0
    genotype = nx.random_tree(n=num_initial_limbs, create_using=nx.DiGraph)

    node_attributes = {}
    for i in range(num_initial_limbs):
        
        node_attributes[i] = generateRandomNodeAttributes(genotype=genotype, low=lowSize, high=highSize)

    nx.set_node_attributes(genotype, node_attributes)

    
    edge_attributes = {}
    for u,v in genotype.edges():
        attributes = generateRandomEdgeAttributes()
        
        edge_attributes[(u,v)] = attributes

    nx.set_edge_attributes(genotype, edge_attributes)
    

    return genotype


def generateRandomNodeAttributes(genotype, low:float, high:float):
    return {
        "length": np.random.uniform(low=low, high=high),
        "width": np.random.uniform(low=low, high=high),
        "height": np.random.uniform(low=low, high=high),
        "recursive_limit": 0,
        "neuron_weights": {edge: np.random.uniform(low=-1, high=1) for edge in list(genotype.edges)}, # this is a dictionary of {(parentNodeId, childNodeId): neuron_weight}, being the neuron weights for all the motors this sensor will connect to (it's fully connected so all the edges of the graph)
        "has_sensor": np.random.choice((True, False), size=(1,))[0]
    }

def generateRandomEdgeAttributes():
    attributes = {
            "length_proportion": np.random.uniform(low=0.05, high=1),
            "width_proportion": np.random.uniform(low=0, high=1),
            "height_proportion": np.random.uniform(low=0, high=1)
        }
    surface_i = np.random.randint(low=0,high=2)
    # make sure the joint is one the surface
    match surface_i:
        case 0:
            attributes["length_proportion"] = 1
        case 1:
            attributes["width_proportion"] = 1
        case 2:
            attributes["height_proportion"] = 1
    
    return attributes



if __name__ == "__main__":
    genotype1 = generateRandomGenotype(3,5, lowSize=0.2, highSize=1)

    print("my genotype:\n", genotype1, "\n", nx.forest_str(genotype1), genotype1.nodes[0])


    build_body1 = BODY_BUILDER(genotype1, 100)

    build_body1.Build_Body()

    os.system("python3 simulate.py GUI 100 False")


# os.system(f"python3 simulate.py GUI 100 False")

"""
GENOTYPE:
1. Graph structure of body parts and joints
2. Nodes:
- length
- width
- height
- recursive_limit
-- when recursive_limit is changed, the neuron weight arrays for all other body parts must be updated to have a connection to this new weight
- has_sensor
- neuron_weights
3. Edges:
- length_proportion
- width_proportion
- height_proportion

MUTATION:
Chance for small change to any of the above parameters (nodes and edges)
THEN
Chance for removal of an outer body part
THEN
Chance for addition of a body part to an outer node

"""







"""
Make creature genotype a direct encoding: 
--> networkx representation of nodes and edges

All joints will have neurons
Neural network will be a simple 2 layer network: all sensors connected to all motors

Change creature generation from a recursive object
TO: a function:
- takes in genotype which denotes the size of objects, position of joints, recursive limit, etc
- uses the classes, but calls their functions manually, not from within the function itself

Mutation function can be a small probability to change every aspect of the creature
--> smaller changes should be more likely than larger changes (using Gaussian noise)
Things to change via mutation:
LIMB:
- length
- width
- height
- recursive_limit
-- when recursive_limit is change, the neuron weight arrays for all other body parts must be updated to have a connection to this new weight
- neuron weights
EDGE:
- length proportion
- width proportion
- height proportion
ADD LIMB:
- to which other body part will it be attached to (new edge to new node)
- random length, width, height, recursive limit, neuron weights to begin
- when a new limb (and joint) is added, the neuron weight arrays for all other body parts must be updated to have a connection to this new joint


Evolution is simply best parent wins...
No sexual reproduction!

"""