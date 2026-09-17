SetFactory("Built-in");

Merge "UFc_meshlab.stl";

// Smooth surface classification to prevent seams and craters
ClassifySurfaces{Pi, 1, 1, Pi};
CreateGeometry;

Surface Loop(1) = Surface{:};
Volume(1) = {1};

// Tag the UFc volume so Abaqus recognizes it
Physical Volume("UFC") = {1};

// --- STRICT 1.0mm UNIFORM SIZING ---
Mesh.MeshSizeMin = 1.0;
Mesh.MeshSizeMax = 1.0;
Mesh.MeshSizeFromPoints = 0;
Mesh.MeshSizeFromCurvature = 0;
Mesh.MeshSizeExtendFromBoundary = 0;

// --- ALGORITHMS FOR PERFECT PROPORTIONS ---
Mesh.Algorithm = 6;   // Forces the beautiful, uniform surface triangles
Mesh.Algorithm3D = 1; // Stable 3D volume filling

// Maximum optimization
Mesh.Optimize = 1;
Mesh.OptimizeNetgen = 1;
Mesh.Smoothing = 100;

// Export strictly the 3D solid to prevent Abaqus errors
Mesh.SaveAll = 0; 

