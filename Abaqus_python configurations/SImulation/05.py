from abaqus import *
from abaqusConstants import *

MODEL = 'FInalModel'
model = mdb.models[MODEL]

part_names = ['PART-1', 'PART-1_1', 'PART-1_2']

for PART in part_names:
    p = model.parts[PART]
    
    # Check if datums exist to avoid errors
    if len(p.datums.keys()) > 0:
        # Get the ID of the datum created in Script 4
        datum_id = max(p.datums.keys())
        
        region = p.sets['ALL_ELEMENTS']
        
        # Delete previous material orientation assignments to avoid conflicts
        while len(p.materialOrientations) > 0:
            del p.materialOrientations[0]

        # Assign the orientation
        p.MaterialOrientation(
            region=region,
            orientationType=SYSTEM,
            axis=AXIS_1, 
            localCsys=p.datums[datum_id],
            fieldName='',
            additionalRotationType=ROTATION_NONE,
            angle=0.0,
            additionalRotationField=''
        )
        
        print('Material orientation assigned to:', PART)
    else:
        print('Error: No datum found for', PART)

print('--------------------------------')
print('SCRIPT 05 FINISHED SUCESSFULLY')
print('--------------------------------')
