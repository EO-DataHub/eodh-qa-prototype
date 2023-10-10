"""example_workflow - script to prototype qa check workflow for EODH"""

import requests
import datetime

__author__ = ["Sam Hunt <sam.hunt@npl.co.uk>", "Sam Malone <samantha.malone@npl.co.uk>"]
__all__ = []


# url for example S2A product STAC item provided by CEDA
STAC_ITEM_URL = "https://api.stac.ceda.ac.uk/eo/collections/Sentinel-2A/items/6d010854a589dd5980442d7947be6233574ab442"


def qacheck_geometry_coords_valid(item: dict) -> dict:
    """
    Checks that `"coordinates"` provided for item `"geometry"` entry valid.

    :param item: STAC record for catalogue item
    :return: check result
    """

    check_result = {}

    return check_result


def main():
    """
    Runs example QA check(s) for defined STAC item
    """

    # Gets example STAC item
    stac_item = requests.get(STAC_ITEM_URL).json()

    # Runs example QA check - this could have arbitrary complexity
    example_check_result = qacheck_geometry_coords_valid(stac_item)

    return None


if __name__ == "__main__":
    main()
