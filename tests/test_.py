
from app.utilities import calculate_overlap
from unittest.mock import patch
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon

@patch('geopandas.read_file')
def test_calculate_overlap_small(mock_read_file):
    # Sample GeoJSON 
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [-123.1738, 37.6398],
                            [-123.1738, 37.9298],
                            [-122.6738, 37.9298],
                            [-122.6738, 37.6398],
                            [-123.1738, 37.6398]
                        ]
                    ]
                }
            }
        ]
    }
    df = pd.DataFrame({
    'Mang_Type': ['DIST', 'FED', 'LOC', 'NGO', 'STAT'],
    'FeatClass': ['Fee', 'Fee', 'Fee', 'Fee', 'Fee'],
    'Des_Tp': ['ACC', 'CONE', 'FORE', 'FOTH', 'HCA'],
    'geometry': [Polygon([(-123.2, 37.6), (-123.2, 37.7), (-123.1, 37.7), (-123.1, 37.6)]), 
                 Polygon([(-123.1, 37.7), (-123.1, 37.8), (-123, 37.8), (-123, 37.7)]), 
                 Polygon([(-122.9, 37.8), (-122.9, 37.9), (-122.8, 37.9), (-122.8, 37.8)]), 
                 Polygon([(-122.8, 37.9), (-122.8, 38), (-122.7, 38), (-122.7, 37.9)]), 
                 Polygon([(-122.7, 38), (-122.7, 38.1), (-122.6, 38.1), (-122.6, 38)])]
})
    gdf = gpd.GeoDataFrame(df, geometry='geometry')
    gdf.set_crs("EPSG:4326", inplace=True)

    mock_read_file.return_value = gdf

    print("DataFrame used for calculation:")
    print(gdf)

    # Expected result 
    expected_result = {
    "Des_Tp": {
        "ACC": 3.059215565518262, 
        "CONE": 6.893292865413912, 
        "FORE": 6.902631447887968, 
        "FOTH": 2.0587971426353975, 
        "HCA": 0
    },
    "FeatClass": {
        "Fee": 18.91393702145554
    },
    "Mang_Type": {
        "DIST": 3.059215565518262, 
        "FED": 6.893292865413912, 
        "LOC": 6.902631447887968, 
        "NGO": 2.0587971426353975, 
        "STAT": 0
    }
}


    result = calculate_overlap(geojson)
    print("Result of calculate_overlap function:")
    print(result)

    # Assert the output is correct
    assert result == expected_result

@patch('geopandas.read_file')
def test_calculate_overlap_no_overlap(mock_read_file):
    # Sample GeoJSON 
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [-105.00432014465332, 39.96167604831683],
                            [-105.00715255737305, 39.95868749291691],
                            [-105.00921249389647, 39.95948888179304],
                            [-105.01067161560059, 39.9602543440034],
                            [-105.01195907592773, 39.9607242332767],
                            [-105.00989913940431, 39.96321407936762],
                            [-105.00758171081543, 39.96275549363738],
                            [-105.00432014465332, 39.96167604831683]
                        ]
                    ]
                }
            }
        ]
    }
    # Mock the return value of geopandas.read_file
    df = pd.DataFrame({
        'Mang_Type': ['DIST', 'FED', 'LOC', 'NGO', 'STAT'],
        'FeatClass': ['Fee', 'Fee', 'Fee', 'Fee', 'Fee'],
        'Des_Tp': ['ACC', 'CONE', 'FORE', 'FOTH', 'HCA'],
        'geometry': [Polygon([(0, 0), (1, 1), (1, 0)]), Polygon([(0, 0), (1, 1), (1, 0)]), Polygon([(0, 0), (1, 1), (1, 0)]), Polygon([(0, 0), (1, 1), (1, 0)]), Polygon([(0, 0), (1, 1), (1, 0)])]
    })
    gdf = gpd.GeoDataFrame(df, geometry='geometry')
    gdf.set_crs("EPSG:4326", inplace=True)
    mock_read_file.return_value = gdf
    

    # Expected result - you'd replace this with the expected output from your function when given the above input
    expected_result = {
    "message": "No overlap found"
    }

    result = calculate_overlap(geojson)

    # Assert the output is correct
    assert result == expected_result

