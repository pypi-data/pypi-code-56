####################################################################
# Name: Alexandra Crowe
# Date: 6 June 2020
# Description: This script defines the functions executed by
# the main.py script. The functions here are arcpy functions that
# create a new feature class based on query parameters set by the
# GUI. 
#####################################################################

def extractSelectiontoNewShapefile(polygonShapefile, targetCountry, countryQuery, pointShapefile, shopQuery, fileName):
    import arcpy
    import os
    arcpy.env.overwriteOutput = True
    #Make a layer from a feature class, select points that intersect that polygon and subset
    #that selection by selecting points with a specified attribute.
    arcpy.MakeFeatureLayer_management (polygonShapefile, targetCountry, countryQuery)
    queryFC = arcpy.SelectLayerByLocation_management(pointShapefile, 'INTERSECT', targetCountry)
    arcpy.SelectLayerByAttribute_management(queryFC, 'SUBSET_SELECTION', shopQuery)
    arcpy.Delete_management(targetCountry)
    # If features matched criteria, write them to a new feature class
    matchcount = int(arcpy.GetCount_management(queryFC)[0])
    if matchcount != 0:
        arcpy.FeatureClassToFeatureClass_conversion(queryFC, os.path.dirname(fileName), os.path.basename(fileName))
        return matchcount

#Create a list of unique values from a attribute field.
def getUniqueValues(table , field):
    import arcpy
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})

def getValidFieldsForShapefile(fileName):
    """produces a list of editable string fields for a Point shapefile with the given name; the list will be empty if no Point based shapefile exists under that name."""
    import arcpy
    import os
    fields = []
    if os.path.exists(fileName):
        desc = arcpy.Describe(fileName)
        try: # trying to access shapeType may throw exception for certain kinds of data sets
            fields = getStringFieldsForDescribeObject(desc)
        except:
            fields = []
    return fields

def getStringFieldsForDescribeObject(desc):
    """produces a list of editable string fields from a given arcpy.Describe object"""
    fields = []
    for field in desc.fields: # go through all fields
        if field.type == 'String' and field.editable:
            fields.append(field.baseName)
    return fields
