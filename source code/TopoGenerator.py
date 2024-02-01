__author__ = "Ali T.Ghomi"


import rhinoscriptsyntax as rs
import Rhino

#------------------------------------------------------------------------
ghenv.Component.Message = "Generates a topography surface from series of curves"
ghenv.Component.Name = "Topo Generator"
ghenv.Component.NickName = "Topo Generator"
ghenv.Component.Category = "AliT Toolkit"
ghenv.Component.SubCategory = "Site"
ghenv.Component.Description = "Generates a topography surface from series of curves. \nThe curves should be in their actual Z hight and for better results they should connect to the boundary curve in plan if they are not closed. \nThe grid_size is an approximation."

#------------------------------------------------------------------
#Generating the surface points based on the boundary
srf = rs.AddPlanarSrf(boundary_crv)
u_domain = rs.SurfaceDomain(srf,0)
v_domain = rs.SurfaceDomain(srf,1)
surface_points = []

u_count = int(round((u_domain[1]-u_domain[0])/grid_size))
v_count = int(round((v_domain[1]-v_domain[0])/grid_size))

u = u_domain[0]
for i in range(u_count):
    v = v_domain[0]
    for j in range(v_count):
        pt = rs.EvaluateSurface(srf,u ,v)
        surface_points.append(pt)
        v = v + (v_domain[1]-v_domain[0])/v_count
    pt_v_end = rs.EvaluateSurface(srf,u ,v_domain[1])
    surface_points.append(pt_v_end)
    u = u + (u_domain[1]-u_domain[0])/u_count
#adding the last row
v = v_domain[0]
for i in range(v_count):
    pt = rs.EvaluateSurface(srf,u_domain[1] ,v)
    surface_points.append(pt)
    v = v + (v_domain[1]-v_domain[0])/v_count
pt_end_corner = rs.EvaluateSurface(srf,u_domain[1] ,v_domain[1]) 
surface_points.append(pt_end_corner)

#----------------------------------------------------------------------------

srf_pts_closest_topo_pts = {}
srf_pts_closest_topo_project_pts = {}
srf_pts_closest_distances = {}
srf_pts_closest_lines = {}
srf_pts_on_topo_curve = []

#project topo curves
projected_topo_curves = []
for crv in topo_curves:
    projected_curve = Rhino.Geometry.Curve.ProjectToPlane(crv, rs.PlaneFromNormal([0,0,0],[0,0,1]))
    projected_topo_curves.append(projected_curve)
    
#list topo curves heights
topo_heights = []
for crv in topo_curves:
    pt = rs.EvaluateCurve(crv,0.5)
    z = pt[2]
    topo_heights.append(z)
    
#find closest points and draw intersection lines for each point on surface
for i in range(len(surface_points)):
    closest_points_projected = []
    distances = []
    lines = []
    is_srf_pts_on_topo_curve = False
    for j in range(len(topo_curves)):
        t = rs.CurveClosestPoint(projected_topo_curves[j],surface_points[i])
        projected_pt = rs.EvaluateCurve(projected_topo_curves[j],t)
        
        #find the distance to the projected points
        distance = rs.Distance(surface_points[i],projected_pt)
        
        #draw lines to the check intersections
        if distance> 0.001:
            line = rs.AddLine(surface_points[i],projected_pt)
            lines.append(line)
            distances.append(distance)
            closest_points_projected.append(projected_pt)
            
        else:
            line = None
            is_srf_pts_on_topo_curve = True
            distances.append(distance)
            closest_points_projected.append(projected_pt)
            lines.append(None)
            break
            
    srf_pts_on_topo_curve.append(is_srf_pts_on_topo_curve)
    srf_pts_closest_topo_project_pts[i] = closest_points_projected
    srf_pts_closest_distances[i] = distances
    srf_pts_closest_lines[i] = lines
    
#------------------------------------------------------------------------------------------------------
#checking intersections and finding the weighted Z and construct the topo points

topo_points = []

for k,v in srf_pts_closest_topo_project_pts.items():
    #checking the intersections
    
    if srf_pts_on_topo_curve[k]:
        #final_z = [x for _, x in sorted(zip(srf_pts_closest_distances[k],topo_heights))][0]
        final_z = topo_heights[len(srf_pts_closest_topo_project_pts[k])-1]
    else:
        topo_ids = []
        
        #Finding the corresponding topo curves
        for i in range(len(v)):
                
            l = srf_pts_closest_lines[k][i]
            intersection = False
            
            for j in range(len(projected_topo_curves)):
                if i != j:
                    if rs.CurveCurveIntersection(l, projected_topo_curves[j]) != None:
                        intersection = True
                        break
            if intersection == False:
                topo_ids.append(i)
                
        #finding the weighted Z
        total_distance_weight = 0
        weighted_Zs = []
        weights = []
        dists = []
        heights = []
        for id in topo_ids:
            dist = srf_pts_closest_distances[k][id]
            heights.append(topo_heights[id])
            dists.append(dist)
        for i in range(len(dists)):
            weight = 1/(dists[i]/sum(dists))
            weights.append(weight)
        for i in range(len(dists)):
            weighted_Zs.append(heights[i]*weights[i]/sum(weights))
        final_z = sum(weighted_Zs)
    #construct new points
    final_pt = rs.AddPoint(surface_points[k][0],surface_points[k][1],final_z)
    topo_points.append(final_pt)
    
topo_surface  = topo_points
#-----------------------------------------------------------------------------------------------------------
#Creating the topo surface iso curves

def curves_from_rows(pts_rows):
    curves = []
    for i in range(len(pts_rows)):
        crv = rs.AddInterpCurve(pts_rows[i])
        curves.append(crv)
    return curves

#Partition the point list into rows
def partition(lst, size):
    sublists = [lst[i:i + size] for i in range(0, len(lst), size)]
    return sublists

def flip_matrix(list_of_lists):
    new_list_of_lists = []
    for i in range(len(list_of_lists[0])):
        new_list = []
        for l in list_of_lists:
            new_list.append(l[i])
        new_list_of_lists.append(new_list)
    return new_list_of_lists
    
points_in_rows = list(partition(topo_points,v_count+1))
u_curves = curves_from_rows(points_in_rows)

flipped_points_in_rows = flip_matrix(points_in_rows)
v_curves = curves_from_rows(flipped_points_in_rows)

#----------------------------------------------------------------------
#Generating the surface

all_crvs = []
all_crvs.extend(u_curves)
all_crvs.extend(v_curves)

topo_srf = rs.AddNetworkSrf(all_crvs)
topo_surface = topo_srf