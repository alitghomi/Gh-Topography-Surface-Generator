<<<<<<< HEAD:source code/TopoGenerator_python.py
﻿__author__ = "Ali T.Ghomi"


import rhinoscriptsyntax as rs
import Rhino

#------------------------------------------------------------------------
ghenv.Component.Message = "Generates a topography surface from series of curves"
ghenv.Component.Name = "Topo Generator"
ghenv.Component.NickName = "Topo Generator"
ghenv.Component.Category = "AliT Toolkit"
ghenv.Component.SubCategory = "Site"
ghenv.Component.Description = "Generates a topography surface from series of curves."

#------------------------------------------------------------------
#Project the boundary curve
projected_boundary_curve = Rhino.Geometry.Curve.ProjectToPlane(boundary_crv, rs.PlaneFromNormal([0,0,0],[0,0,1]))

#Generating the surface points based on the boundary
srf = rs.AddPlanarSrf([projected_boundary_curve])
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
        if len(topo_ids) > 0:
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
        else:
            final_z = topo_heights[id]
        
    #construct new points
    final_pt = rs.AddPoint(surface_points[k][0],surface_points[k][1],final_z)
    
    topo_points.append(final_pt)
    
#-----------------------------------------------------------------------------------------------------------
topo_srf = rs.AddSrfControlPtGrid([u_count+1,v_count+1],topo_points)
topo_surface = topo_srf

=======
﻿__author__ = "Ali T.Ghomi"


import rhinoscriptsyntax as rs
import Rhino

#------------------------------------------------------------------------
ghenv.Component.Message = "Generates a topography surface from series of curves"
ghenv.Component.Name = "Topo Generator"
ghenv.Component.NickName = "Topo Generator"
ghenv.Component.Category = "AliT Toolkit"
ghenv.Component.SubCategory = "Site"
ghenv.Component.Description = "Generates a topography surface from series of curves."

#------------------------------------------------------------------
#Project the boundary curve
projected_boundary_curve = Rhino.Geometry.Curve.ProjectToPlane(boundary_crv, rs.PlaneFromNormal([0,0,0],[0,0,1]))

#Generating the surface points based on the boundary
srf = rs.AddPlanarSrf([projected_boundary_curve])
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
        if len(topo_ids) > 0:
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
        else:
            final_z = topo_heights[id]
        
    #construct new points
    final_pt = rs.AddPoint(surface_points[k][0],surface_points[k][1],final_z)
    
    topo_points.append(final_pt)
    
#-----------------------------------------------------------------------------------------------------------
topo_srf = rs.AddSrfControlPtGrid([u_count+1,v_count+1],topo_points)
topo_surface = topo_srf

>>>>>>> db9cc40b42486e9bfc43ec74fe12abf3dda263e1:source code/TopoGenerator.py
