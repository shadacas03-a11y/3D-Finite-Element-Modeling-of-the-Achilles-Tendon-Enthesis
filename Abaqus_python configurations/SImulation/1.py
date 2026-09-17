from abaqus import *
from abaqusConstants import *

model = mdb.models['FInalModel']
a = model.rootAssembly

instT = a.instances['PART-1-1']
instU = a.instances['PART-1_1-1']
instC = a.instances['PART-1_2-1']

# 1. Limpiar superficies
for name in ['Surf_Tendon', 'Surf_UFc_Top', 'Surf_UFc_Bottom', 'Surf_CFc']:
    if name in a.surfaces.keys(): del a.surfaces[name]

# 2. Extraer caras
def get_exterior_faces(inst):
    face_count = {}
    face_objects = {}
    for elem in inst.elements:
        nodes = elem.getNodes()
        # Para C3D4, los índices 0,1,2,3 corresponden a FACE1, FACE2, FACE3, FACE4
        for face_index, inds in enumerate([(0,1,2), (0,1,3), (0,2,3), (1,2,3)]):
            n1, n2, n3 = nodes[inds[0]], nodes[inds[1]], nodes[inds[2]]
            key = tuple(sorted([n1.label, n2.label, n3.label]))
            
            if key not in face_count:
                face_count[key] = 0
                face_objects[key] = (elem.label, face_index, n1, n2, n3)
            face_count[key] += 1
            
    ext_faces = []
    for key, count in face_count.items():
        if count == 1:
            ext_faces.append(face_objects[key])
    return ext_faces

print('\n==============================================')
print('1. OBTENIENDO CARAS EXTERIORES')
print('==============================================')
extT = get_exterior_faces(instT)
extU = get_exterior_faces(instU)
extC = get_exterior_faces(instC)

# 3. Filtrar
def filter_and_build_kwargs(inst_origen, ext_faces, target_z, inst_destino, tol_z=1.5):
    ref_xs = [n.coordinates[0] for n in inst_destino.nodes]
    ref_ys = [n.coordinates[1] for n in inst_destino.nodes]
    min_x, max_x = min(ref_xs) - 1.0, max(ref_xs) + 1.0
    min_y, max_y = min(ref_ys) - 1.0, max(ref_ys) + 1.0
    

    face_labels = {1: [], 2: [], 3: [], 4: []}
    count = 0
    
    for f in ext_faces:
        elem_label = f[0]
        face_idx = f[1] # 0 a 3, corresponde a FACE1 a FACE4
        n1, n2, n3 = f[2], f[3], f[4]
        
        cx = (n1.coordinates[0] + n2.coordinates[0] + n3.coordinates[0]) / 3.0
        cy = (n1.coordinates[1] + n2.coordinates[1] + n3.coordinates[1]) / 3.0
        cz = (n1.coordinates[2] + n2.coordinates[2] + n3.coordinates[2]) / 3.0
        
        if abs(cz - target_z) < tol_z:
            if min_x <= cx <= max_x and min_y <= cy <= max_y:
                face_labels[face_idx + 1].append(elem_label)
                count += 1
                
    kwargs = {}
    if face_labels[1]: kwargs['face1Elements'] = inst_origen.elements.sequenceFromLabels(face_labels[1])
    if face_labels[2]: kwargs['face2Elements'] = inst_origen.elements.sequenceFromLabels(face_labels[2])
    if face_labels[3]: kwargs['face3Elements'] = inst_origen.elements.sequenceFromLabels(face_labels[3])
    if face_labels[4]: kwargs['face4Elements'] = inst_origen.elements.sequenceFromLabels(face_labels[4])
    
    return count, kwargs

print('\n==============================================')
print('2. AGRUPANDO ELEMENTOS POR CARA (FACE1...FACE4)')
print('==============================================')
count_T_bot, kw_T_bot = filter_and_build_kwargs(instT, extT, -9.8, instU)
count_U_top, kw_U_top = filter_and_build_kwargs(instU, extU, -8.3, instT)
count_U_bot, kw_U_bot = filter_and_build_kwargs(instU, extU, -25.3, instC)
count_C_top, kw_C_top = filter_and_build_kwargs(instC, extC, -17.8, instU)

print('Caras para Surf_Tendon      =', count_T_bot)
print('Caras para Surf_UFc_Top     =', count_U_top)
print('Caras para Surf_UFc_Bottom  =', count_U_bot)
print('Caras para Surf_CFc         =', count_C_top)

print('\n==============================================')
print('3. CREANDO SUPERFICIES')
print('==============================================')
if count_T_bot > 0: a.Surface(name='Surf_Tendon', **kw_T_bot)
if count_U_top > 0: a.Surface(name='Surf_UFc_Top', **kw_U_top)
if count_U_bot > 0: a.Surface(name='Surf_UFc_Bottom', **kw_U_bot)
if count_C_top > 0: a.Surface(name='Surf_CFc', **kw_C_top)

print('Done.')
