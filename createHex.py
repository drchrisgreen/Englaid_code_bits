import os
import arcpy
from arcpy import env
from math import sqrt as sqrt

def process(studyarea,size,outfile):
	
	working_dir = 'Z:/Documents/temp/'
	env.workspace = working_dir
	out_path = working_dir
	
	# get extent of studyarea layer
	sa = 'Z:/Documents/temp/' + studyarea + '.shp'
	desc = arcpy.Describe(sa)
	min_X = desc.Extent.XMin
	max_X = desc.Extent.XMax
	min_Y = desc.Extent.YMin
	max_Y = desc.Extent.YMax
	
	# determine start and end points
	start_X = (int(min_X / size) * size) - (size * 3)
	start_Y = (int(min_Y / size) * size) - (size * 3)
	end_X = (int(max_X / size) * size) + (size * 3)
	end_Y = (int(max_Y / size) * size) + (size * 3)
	
	# generate point layer
	out_name = 'temp_points.shp'
	geometry_type = 'POINT'
	spatial_reference = arcpy.SpatialReference('C:\Program Files\ArcGIS\Desktop10.0\Coordinate Systems\Projected Coordinate Systems\National Grids\Europe\British National Grid.prj')
	outPoints = arcpy.CreateFeatureclass_management(out_path, out_name, geometry_type, '', 'DISABLED', 'DISABLED', spatial_reference)
	arcpy.AddField_management(outPoints,'hexID','LONG')
	rows = arcpy.InsertCursor(outPoints)
	
	currentId = 0
	current_X = start_X
	current_Y = start_Y
	x_diff = sqrt((size*size)-((size/2)*(size/2)))
	
	odd = 0
	while current_X <= end_X:
		x = current_X
		if odd == 0:
			current_Y = start_Y
			odd = 1
		else:
			current_Y = start_Y + (size / 2)
			odd = 0
		while current_Y <= end_Y:
			y = current_Y
			newpoint = arcpy.Point()
			newpoint.X = float(x)
			newpoint.Y = float(y)
			row = rows.newRow()
			row.hexID = int(currentId)
			row.shape = newpoint
			rows.insertRow(row)
			currentId += 1
			current_Y += size
		current_X += x_diff
	
	# generate thiessen polys
	outThiessen = out_path + 'temp_thiessen.shp'
	outFields = "ALL"
	arcpy.CreateThiessenPolygons_analysis(outPoints, outThiessen, outFields)
	
	# select hexes based on overlap with studyarea and export
	arcpy.MakeFeatureLayer_management(outThiessen, 'tempLyr') 
	arcpy.SelectLayerByLocation_management('tempLyr', 'intersect', sa)
	matchcount = int(arcpy.GetCount_management('tempLyr').getOutput(0)) 
	if matchcount == 0:
		print('no features matched spatial criteria')
	else:
		arcpy.CopyFeatures_management('tempLyr', out_path + outfile + '.shp')
	
	# delete point layer and unfiltered hexes
	arcpy.Delete_management(outPoints)
	arcpy.Delete_management(outThiessen)
	arcpy.Delete_management('tempLyr')