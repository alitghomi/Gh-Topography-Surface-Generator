# Topography Surface Generator

![](https://github.com/alitghomi/Gh-Topography-Surface-Generator/blob/main/assets/topo_icon_180.png)

## GHPython component to generate NURBS topography surface


## How to use
### How to open
You can drag and drop the .ghpy file inside the component folder into the Grasshopper environment. Then you can find the component in the AliT Toolkit > Site in the Grasshopper tabs. Or you can use the source .gh file in the /source code folder.

### Inputs
#### topo_curves
A list of topography contour curves in their actual height.

#### boundary_crv
A planar rectangle curve describing the boundaries of the generated surface.

#### grid_size
An approximate distance between control points. Smaller number results in a more accurate surface but it also takes more time to calculate. 

### Outputs

#### topo_surface
A NURBS surface generated from the network of u_curves and v_curves.

#### u_curves
A series of curves following the topography in u direction

#### v_curves
A series of curves following the topography in v direction

### Notes
- The code is developed and tested in Rhino 7
- The code is written in Grasshopper default Python component.
- The current version calculates the surface points' height based on a weighted average of its distance to the topography curves. This results in a linear change in height. Probebly a non-leniear fomula would fill the gaps more naturally but that's for another day.
