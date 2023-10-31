"""eodh_qa_prototype.qa_check_workflows.stac_geometry_coordinates - validation for the STAC item geometry coordinates"""

from typing import Tuple
import datetime as dt
from eodh_qa_prototype.qa_check_workflows.base import BaseQACheckWorkFlow

__author__ = "Sam Hunt <sam.hunt@npl.co.uk>"
__all__ = ["QACheckSTACItemGeomCoords"]


class QACheckSTACItemGeomCoords(BaseQACheckWorkFlow):
    name = "stac_item_geom_coords"
    version = "1.0"

    def run_check(self, item: dict) -> Tuple[dict, dict]:
        """
        Checks that `"coordinates"` provided for STAC item `"geometry"` entry valid.

        :param item: STAC record for catalogue item
        :return: check result and ancillary info
        """

        # Gets coordinate data from the example STAC item file
        geometry_coords = item['geometry']['coordinates']

        # Check values are within bounds for valid coordinate data
        coords_valid = [False] * len(geometry_coords)
        for i, coord_i in enumerate(geometry_coords):
            if (-90 <= coord_i[0][0] <= 90) and (-180 <= coord_i[0][1] <= 180):
                coords_valid[i] = True

        valid_check = all(coords_valid)

        # Dicionary including check and other metadata (version, software env etc)
        check_result = {
            "result": valid_check,
            "result_vocab": "vocab/url",
            "check_datetime": dt.datetime.now().strftime("%Y%m%dT%H%M"),
            "check_name": self.name,
            "check_author": __author__,
            "check_version": self.version,
            "ref_url": {},
        }

        return check_result, {}

if __name__ == "__main__":
    pass
