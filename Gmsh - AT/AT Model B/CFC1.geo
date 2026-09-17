SetFactory("Built-in");

Merge "CFc_meshlab.stl";

// Smooth surface classification to prevent seams
ClassifySurfaces{Pi, 1, 1, Pi};
CreateGeometry;

Surface Loop(1) = Surface{:};
Volume(1) = {1};

// Tag the CFc volume
Physical Volume("CFC") = {1};

// --- STRICT 1.0mm UNIFORM SIZING ---
Mesh.MeshSizeMin = 1.0;
Mesh.MeshSizeMax = 1.0;
// These force Gmsh to ignore the old STL triangle sizes
Mesh.MeshSizeFromPoints = 0;
Mesh.MeshSizeFromCurvature = 0;
Mesh.MeshSizeExtendFromBoundary = 0;

// --- ALGORITHMS FOR PERFECT PROPORTIONS ---
Mesh.Algorithm = 6;   // Forces perfectly uniform surface triangles
Mesh.Algorithm3D = 1; // Fills the solid securely

// Maximum optimization for element quality
Mesh.Optimize = 1;
Mesh.OptimizeNetgen = 1;
Mesh.Smoothing = 100;

// CRITICAL FIX: Prevents Abaqus from importing 1D wires or 2D surfaces
Mesh.SaveAll = 0; 

