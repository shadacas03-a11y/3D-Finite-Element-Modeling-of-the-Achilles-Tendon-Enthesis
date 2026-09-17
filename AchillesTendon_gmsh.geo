Merge "AchillesTendon_meshlab.stl";

Geometry.Tolerance = 1e-3;

Mesh.MeshSizeMin = 0.8;
Mesh.MeshSizeMax = 1.2;

Mesh.MeshSizeFromCurvature = 0;
Mesh.MeshSizeFromPoints = 0;
Mesh.MeshSizeExtendFromBoundary = 0;

ClassifySurfaces{40*Pi/180, 1, 1, 180*Pi/180};
CreateGeometry;
Coherence;

Surface Loop(1) = Surface{:};
Volume(1) = {1};

Mesh.Algorithm3D = 10;
Mesh.ElementOrder = 1;

Mesh.Optimize = 1;
Mesh.OptimizeNetgen = 1;
Mesh.Smoothing = 10;

Mesh 3;

Save "AchillesTendon_volume_mesh.inp";