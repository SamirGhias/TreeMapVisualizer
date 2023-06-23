# TreeMapVisualizer
In CSC148 we were tasked with creating a Python program that sets up and renders an interactive visualization of a given file hierarchy/ population data Using PyGame and a recursive tree class.

We were provided a simple explanation of an algorithm required to generate the dimensions of rectangles and given the following requirements to fulfill.


# Task 1: File Hierarchy Visualization
- scan through any given nested file folder and recursively generate an Abstract tree mirroring the structure 1 to 1, with parent, root, and children nodes as well as the size attribute.
- Run a secondary algorithm that processes the tree generated from the previous step and instantiates a unique rectangle object with dimensions and coordinates for each node in the tree, with the size of the rectangle representing the file size in bytes.
- Start PyGame and render all the rectangles while listening for mouse or keyboard clicks on the PyGame window. Clicking on any rectangle must return the x and y coordinates with which we can backtrack through the tree using the algorithm and locate the exact rectangle underneath the clicked pixel.
- Display the pathname (or country name) from the root alongside the file (or population) size.

- Implemented the following commands:
- Pressing the Up or Down arrow keys increases/decreases the size attribute of the selected rectangle.
- Right-clicking on the rectangle immediately deletes the node from the tree and uses an algorithm to move the deleted nodes' subtrees to their respective parent node.
- Upon any of the above commands, immediately re-run the initial tree generation and rectangle creation algorithms to instantly re-render the screen with newly designated sizes and ratios. The runtime of our algorithms was tested to be efficient in time and spacial complexity.

# Demo Visualization of Nested Files
![](https://github.com/SamirGhias/TreeMapVisualizer/blob/main/gifs/Assignments%20Folder%20demo.gif)


# Task 2: Augmented Code for Viewing Country Population Data:
I made use of the Abstract tree class in task 1 to test the ability to reuse code for an identical requirement. 

Instead of scanning a file folder it simply parses the regions.json and populations.json files, with the parent node as the world and further divided into regions and countries with populations as the (size) attribute. 
The same functionality and interactivity were required with no effect on runtime. 

# Demo of Population Data 
![](https://github.com/SamirGhias/TreeMapVisualizer/blob/main/gifs/population%20gif.gif)
