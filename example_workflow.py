"""example_workflow - script to prototype qa check workflow for EODH"""

import requests
import datetime as dt
import json

__author__ = ["Sam Hunt <sam.hunt@npl.co.uk>", "Sam Malone <samantha.malone@npl.co.uk>"]
__all__ = []
__version__ = "0.1"


# url for example S2A product STAC item provided by CEDA
STAC_ITEM_URL = "https://api.stac.ceda.ac.uk/eo/collections/Sentinel-2A/items/6d010854a589dd5980442d7947be6233574ab442"

# example STAC item json - to use before fixing url SSL error due to NPLs firewall
STAC_ITEM_JSON = json.dumps({"type": "Feature", "stac_version": "1.0.0", "stac_extensions": [],
             "id": "6d010854a589dd5980442d7947be6233574ab442", "collection": "Sentinel-2A", "bbox": 'null',
             "geometry": {"type": "Polygon", "orientation": "counterclockwise", "coordinates": [
                 [[58.8162812265457, 60.42407827988155], [58.76318311731193, 59.438625858979684],
                  [60.69570505815484, 59.39819844853761], [60.806751716111265, 60.382025432644134],
                  [58.8162812265457, 60.42407827988155]]]}, "properties": {
        "platform": {"Platform Family Name": "SENTINEL", "NSSDC Identifier": "2015-000A",
                     "Instrument Family Name": "Multi-Spectral Instrument", "Instrument Abbreviation": "MSI",
                     "Platform Number": "2A", "Mission": "Sentinel-2", "Satellite": "Sentinel-2A",
                     "Family": "SENTINEL-2A"},
        "orbit_info": {"Start Relative Orbit Number": "049", "Start Orbit Number": "016920"},
        "product_info": {"Name": "S2A_MSIL1C_20180918T072611_N0206_R049_T40VFM_20180918T085856"}, "size": 57831,
        "location": "on_tape", "datetime": 'null', "start_datetime": "2018-09-18T07:26:11.024Z",
        "end_datetime": "2018-09-18T07:26:11.024Z"}, "links": [{"rel": "self", "type": "application/geo+json",
                                                                "href": "https://api.stac.ceda.ac.uk/eo/collections/"
                                                                        "Sentinel-2A/items/6d010854a589dd5980442d7947be6233574ab442"},
                                                               {"rel": "parent", "type": "application/json",
                                                                "href": "https://api.stac.ceda.ac.uk/eo/collections/Sentinel-2A"},
                                                               {"rel": "collection", "type": "application/json",
                                                                "href": "https://api.stac.ceda.ac.uk/eo/collections/Sentinel-2A"},
                                                               {"rel": "root", "type": "application/json",
                                                                "href": "https://api.stac.ceda.ac.uk/eo/"}], "assets": {
        "data_file": {
            "href": "https://dap.ceda.ac.uk/neodc/sentinel2a/data/L1C_MSI/2018/09/18/S2A_MSIL1C_20180918T072611_N0206_R049_T40VFM_20180918T085856.zip",
            "title": "S2A_MSIL1C_20180918T072611_N0206_R049_T40VFM_20180918T085856.zip", "type": "application/zip",
            "roles": ["data"]}, "metadata_file": {
            "href": "https://dap.ceda.ac.uk/neodc/sentinel2a/data/L1C_MSI/2018/09/18/S2A_MSIL1C_20180918T072611_N0206_R049_T40VFM_20180918T085856.manifest",
            "title": "S2A_MSIL1C_20180918T072611_N0206_R049_T40VFM_20180918T085856.manifest", "type": "application/xml",
            "roles": ["metadata"]}, "quicklook_file": {
            "href": "https://dap.ceda.ac.uk/neodc/sentinel2a/data/L1C_MSI/2018/09/18/S2A_MSIL1C_20180918T072611_N0206_R049_T40VFM_20180918T085856.png",
            "title": "S2A_MSIL1C_20180918T072611_N0206_R049_T40VFM_20180918T085856.png", "type": "image/png",
            "roles": ["thumbnail"]}}})


def qacheck_geometry_coords_valid(item: dict) -> dict:
    """
    Checks that `"coordinates"` provided for item `"geometry"` entry valid.

    :param item: STAC record for catalogue item
    :return: check result
    """

    # Gets coordinate data from the example STAC item file
    geometry_coords = item['geometry']['coordinates']

    # Check values are within bounds for valid coordinate data
    coords_valid = [False] * len(geometry_coords)
    for i, coord_i in enumerate(geometry_coords):
        if (-90 <= coord_i[0][0] <= 90) and (-180 <= coord_i[0][1] <= 180):
            coords_valid[i] = True

    valid_check = True if all(coords_valid) else False

    # Date QA check was made as a string
    date_of_check = dt.datetime.now().strftime("%Y%m%dT%H%M")

    # Author of check
    author = str(__author__)

    # Link to reference site
    reference_link = 'reference_url'

    # Software version
    software_version = __version__

    # Dicionary including check and other metadata (version, software env etc)
    check_result = {
        "result": valid_check,
        "datetime": date_of_check,
        "author": author,
        "reference_documents": reference_link,
        "software_version": software_version
    }

    return check_result


def main():
    """
    Runs example QA check(s) for defined STAC item
    """

    # Gets example STAC item
    # stac_item = requests.get(STAC_ITEM_URL).json()  # use when SSL error is fixed due to NPLs firewall
    stac_item = json.loads(STAC_ITEM_JSON)

    # Runs example QA check - this could have arbitrary complexity
    example_check_result = qacheck_geometry_coords_valid(stac_item)

    return example_check_result


if __name__ == "__main__":
    print(main())
