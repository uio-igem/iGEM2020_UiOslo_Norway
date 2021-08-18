# -----------------------------------------------------------------------------------------------------------------
# Script using blenderPy's functions to import 3D objects into Blender
# and give them XYZ coordinates from a .CSV file.
# Tested in blender
#
# Video How-To : https://2020.igem.org/wiki/images/6/6f/T--UiOslo_Norway--DemonstrationVideoTEXTandLogo.mp4
# Repository   : https://github.com/uio-igem/iGEM2020_UiOslo_Norway
# Written during iGEM 2020 and improved upon in iGEM 2021
#
# (C) 2020 Joanas Grønbakken, Martin Eide Lien, Norway. Sal.Coli 
# (C) 2021 Martin Eide Lien, Trondheim, Norway. SulFind
# Released under GNU Public License (GPL)
# <NTNU igem github link her >
# email meidelien@gmail.com
# -----------------------------------------------------------------------------------------------------------------



import csv
import bpy


### OS independent blenderScript Parameters ###
"""
By default, blenderScript.py imports 10 objects from "dataForVisualization.CSV" to make it easier to run on low-powered computers.
iGEMSchoolingModel.jl by default outputs data for 100 objects. By changing the integer value of

N_obj = 10 

to

N_obj = 100 

you can import all default created objects.

"""
N_obj = 10 # Number of objects

dim = 3 # Number of dimensions that the objects hould move in

scale = 10 # Divides positions by scale such that fish are closer togheter

importObject = True # Set true if you want to import an .obj file that is suppose to be copied

CopySelected = True  # Set true if you want to copy a object that is selected with the cursor, see


""" 
Model and CSV import information
File path for import, the name of the imported object has to contain name_space
By default, it is <name_space="salmon"> but can changed in a line below.

The objects that are important or copied will only be found if their name 
matches the string inside name space. this is not case sensitive

File path to the . that contains the locations of each object at each time frame.
Each line contains a frame, first entry is a time stamp or some other information.
then the next tree entries in that line are [x,y,z] positions 

"""

########    LINUX           #######
# Comment out lines csv_loc & obj_loc below if you are using this script in a Windows environment

### CSV location ####
# csv_loc= '/home/USERNAME/iGEM2020_UiOslo_Norway/Example data for visualization and analysis/dataForVisualization.CSV'  # Linux .CSV location format

### OBJ location ###
# obj_loc = '/home/USERNAME/iGEM2020_UiOslo_Norway/SALMON.obj' # Linux .OBJ location format


########    LINUX END        #######

"""
########################################################################################

"""

########      WINDOWS        #######
# Comment out lines csv_loc & obj_loc below if you are using this script in a Linux environment

### CSV location ####
csv_loc = 'C:/Users/meide/Documents/GitHub/iGEM2020_UiOslo_Norway/Example data for visualization and analysis/dataForVisualization.CSV' # Windows .CSV location format

### OBJ location ###
obj_loc = 'C:/Users/meide/Documents/GitHub/iGEM2020_UiOslo_Norway/SALMON.obj' # Windows .OBJ location format 


########    WINDOWS END       #######

# The objects that are important or copied will only be found if their name 
# contains this name space, this is not case sensitive
name_space="salmon"


# Imports object 
if importObject:
    # Import a configurable number of objects objects and put them in scene
    for i in range(N_obj):
        new_obj = bpy.ops.import_scene.obj(filepath=obj_loc)
        
        
        
if CopySelected:
    # The scene that imported objects will be placed in
    scn = bpy.context.scene.collection
    
    # Object that we are going to copy, this is selected on the gui by the user
    src_obj = bpy.context.active_object
    
    # For N-1 we copy our object, -1 since we have one from before
    for i in range (N_obj-1):
        new_obj = src_obj.copy()
        # Change name such that the object can be found by it later
        new_obj.name= "Salmon"
        # Copy object data
        new_obj.data = src_obj.data.copy()
        # Clear animation data
        new_obj.animation_data_clear()
        # Set the object in our scene
        scn.objects.link(new_obj)
    



# Array hold the objects that we want to animate
our_objects=[]
# Loop over all objects in scene
for ob in bpy.context.scene.objects:
    # Checks if object has the right name, not case sensitive
    if name_space.lower() in ob.name.lower():
        # Append to array
        our_objects.append(ob)



# Frame number
frame_num=1
# Open csv 
with open(csv_loc, 'r', newline='') as csvfile:
    # our file 
    current_file = csv.reader(csvfile, delimiter=',')
    
    # For each line (row) in current file
    for line in current_file:
        # f takes the time stamp first entry, then *pos contains all our positions 
        f, *pos = line
        
        # Convert positional values to floats
        fpos = [float(p) for p in pos]
        # Initialize array to hold coordinates
        coordinates=[]
        
        # For dim*N_obj append positional values for each agent to the coordinate array
        if dim==3:
            i=0
            while (i<(3*N_obj-2)): 
                temp_pos=[fpos[i]/scale,fpos[i+1]/scale,fpos[i+2]/scale]
                coordinates.append(temp_pos)
                i=i+3
                
        #if dimension equals 2 then set z=0
        if dim==2:
            i=0
            while (i<(3*N_obj-1)):  
                temp_pos=[fpos[i]/scale,fpos[i+1]/scale,0]
                coordinates.append(temp_pos)
                i=i+2
        
        # Set frame
        bpy.context.scene.frame_set(frame_num)
        # For each object and position 
        for ob, position in zip(our_objects, coordinates):
            # Assign new position
            ob.location = position
            # Save frame
            ob.keyframe_insert(data_path="location", index=-1)
        # Count frame number
        frame_num+=1
        
        
#Special thanks to zeffii at stackexchange, for a good answer to a similar problem.