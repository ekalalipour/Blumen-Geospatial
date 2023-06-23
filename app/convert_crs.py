# import geopandas as gpd

# def crs_conversion():
#     # Load the PAD-US data
#     padus = gpd.read_file("../PADUS3/PADUS3_0Geopackage.gpkg")

#     # Convert the CRS to EPSG:4326
#     padus = padus.to_crs(epsg=3857)

#     # Save the converted data to a new file
#     padus.to_file("../PADUS3/PADUS3_0Geopackage_4326.gpkg", driver='GPKG')

# if __name__ == "__main__":
#     crs_conversion()

