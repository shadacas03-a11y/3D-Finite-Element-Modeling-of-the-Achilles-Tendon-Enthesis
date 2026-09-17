from abaqus import *
from abaqusConstants import *

model = mdb.models['FInalModel']
a = model.rootAssembly

instT = a.instances['PART-1-1']      
instU = a.instances['PART-1_1-1']    
instC = a.instances['PART-1_2-1']    

# 1. Clean previous constraints to avoid conflicts
for name in ['Surf_Tendon', 'Surf_UFc_Top', 'Surf_UFc_Bottom', 'Surf_CFc']:
    if name in a.surfaces.keys(): del a.surfaces[name]
for name in ['TIE_TENDON_UFC', 'TIE_UFC_CFC']:
    if name in model.constraints.keys(): del model.constraints[name]

# 2. Function to extract faces by directly accessing node objects
def get_interface_faces(inst, interface_type):
    all_z = [n.coordinates[2] for n in inst.nodes]
    target_z = min(all_z) if interface_type == 'bottom' else max(all_z)
    tol = 0.5 
    
    face_count = {}
    face_objects = {}
    
    for elem in inst.elements:
        nodes = elem.getNodes() # Directly gets the MeshNode objects
        for face_index, inds in enumerate([(0,1,2), (0,1,3), (0,2,3), (1,2,3)]):
            n1, n2, n3 = nodes[inds[0]], nodes[inds[1]], nodes[inds[2]]
            
            # Use labels just to create a unique identifier key for the face
            key = tuple(sorted([n1.label, n2.label, n3.label]))
            
            if key not in face_count:
                face_count[key] = 0
                # Store the actual node objects, completely avoiding getFromLabel later
                face_objects[key] = (elem.label, face_index, n1, n2, n3)
            face_count[key] += 1
            
    selected_faces = []
    
    for key, count in face_count.items():
        if count == 1:
            _, _, n1, n2, n3 = face_objects[key]
            
            # Calculate centroid directly from the stored nodes
            centroid_z = (n1.coordinates[2] + n2.coordinates[2] + n3.coordinates[2]) / 3.0
            
            if abs(centroid_z - target_z) < tol:
                selected_faces.append(inst.elementFaces[face_objects[key][0] - 1])
                
    return selected_faces

print('\n==============================================')
print('EXTRACTING INTERFACES VIA DIRECT NODE OBJECTS')
print('==============================================')

# 3. Extract the faces
faces_T_bot = get_interface_faces(instT, 'bottom')
faces_U_top = get_interface_faces(instU, 'top')
faces_U_bot = get_interface_faces(instU, 'bottom')
faces_C_top = get_interface_faces(instC, 'top')

# 4. Construct Surfaces
if faces_T_bot: a.Surface(name='Surf_Tendon', side1Faces=faces_T_bot)
if faces_U_top: a.Surface(name='Surf_UFc_Top', side1Faces=faces_U_top)
if faces_U_bot: a.Surface(name='Surf_UFc_Bottom', side1Faces=faces_U_bot)
if faces_C_top: a.Surface(name='Surf_CFc', side1Faces=faces_C_top)

print('Captured Surf_Tendon:', len(faces_T_bot))
print('Captured Surf_UFc_Top:', len(faces_U_top))
print('Captured Surf_UFc_Bottom:', len(faces_U_bot))
print('Captured Surf_CFc:', len(faces_C_top))

# 5. Apply Ties
if len(faces_T_bot) > 0 and len(faces_U_top) > 0:
    model.Tie(name='TIE_TENDON_UFC', main=a.surfaces['Surf_Tendon'], secondary=a.surfaces['Surf_UFc_Top'], positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)
    print('--> SUCCESS: TIE_TENDON_UFC Created')
else:
    print('--> ERROR: Tie 1 surfaces missing')

if len(faces_U_bot) > 0 and len(faces_C_top) > 0:
    model.Tie(name='TIE_UFC_CFC', main=a.surfaces['Surf_UFc_Bottom'], secondary=a.surfaces['Surf_CFc'], positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)
    print('--> SUCCESS: TIE_UFC_CFC Created')
else:
    print('--> ERROR: Tie 2 surfaces missing')

print('\n==============================================')
print('DONE!')
print('==============================================')
