import geopandas as gpd
from shapely.geometry import shape


US_SIZE = 9_147_643_000_000 # square meters
FOUR_STATES_SIZE = 801_833_000_000 # square meters CA_OR_NV_WA
CALIFORNIA_SIZE = 403_882_000_000 # square meters

def calculate_overlap(geojson):
    # Extract the geometries from the GeoJSON features
    geometries = [shape(feature["geometry"]) for feature in geojson["features"]]

    # Convert the geometries to a GeoDataFrame
    aoi = gpd.GeoDataFrame(geometry=geometries, crs="EPSG:4326")
    
    # Calculate the area of the AOI
    aoi_area = aoi.to_crs(epsg=3857).area.sum()

    # Check the size of the AOI
    if aoi_area > US_SIZE:
        return {"message": "AOI size exceeds limit. Please make your AOI smaller."}
    elif aoi_area > FOUR_STATES_SIZE:
        print("Warning: This is a very large AOI.")
    elif aoi_area > CALIFORNIA_SIZE:
        print("Note: This is a large AOI.")


    padus_4326 = gpd.read_file('PADUS3/PADUS3_0Geopackage_4326.gpkg')

    # padus_4326 = gpd.read_file("./PADUS3/PADUS3_0Geopackage_4326.gpkg")
    print("Converted PAD-US CRS: ", padus_4326.crs)

    # Calculate the intersection of the AOI with the PAD-US data
    overlap = gpd.overlay(padus_4326, aoi, how='intersection')
    
    if overlap.empty:
        return {"message": "No overlap found"}
        
    # Calculate the area of the overlap for each feature
    overlap['area'] = overlap.to_crs(epsg=3857).area

    result = {}
    for column in ['Mang_Type', 'FeatClass', 'Des_Tp']:
        # Calculate the total area of overlap for each category in the column
        overlap_areas = overlap.groupby(column)['area'].sum()

        # Calculate the percentage overlap for each category
        result[column] = {category: (area / aoi_area) * 100 for category, area in overlap_areas.items()}

        # Add 0% for categories in PAD-US that did not appear in the overlap
        all_categories = set(padus_4326[column].unique())
        for category in all_categories - result[column].keys():
            result[column][category] = 0

        print(f"{column} overlap data: ", result[column])   
        
    return result
