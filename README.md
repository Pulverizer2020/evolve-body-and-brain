# Generating 3d Creatures

Generate random 3d creatures.

Make using [pybullet](https://pybullet.org/wordpress/index.php/forum-2/) & [pyrosim](https://github.com/jbongard/pyrosim) libraries.

# Demo

[Youtube Video:](https://youtu.be/9jaJ_KYywTY)

[![Watch the video](https://img.youtube.com/vi/9jaJ_KYywTY/hqdefault.jpg)](https://youtu.be/9jaJ_KYywTY)

# Running the Code

After installing pyrosim and pybullet, clonse this repository and navigate to this directory. Now run `python3 buildbody.py`. This will generate a random 3D creature. You can change the number of segments and diversions the creatures has by adding `BODY_NODE` and `BODY_EDGE` and changing the `recursive_limit`.

# Structure of Code

The 3d creature's genotype is defined as a graph, where nodes represent body parts and edges represent connections between those body parts. Using this representation, any creature body can be generated. A simple creature might be a repeating body segment, each one with a leg:

<img src="images/Picture1.png" width="200">

The recursive edge is regulated by a `self.recursive_limit` attribute in `BODY_NODE` which limits the number of times a body part can connect to itself.
