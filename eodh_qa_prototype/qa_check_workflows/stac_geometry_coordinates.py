"""eodh_qa_prototype.qa_check_workflows.stac_geometry_coordinates - validation for the STAC item geometry coordinates"""

from typing import Tuple
from eodh_qa_prototype.qa_check_workflows.base import BaseQACheckWorkFlow

__author__ = "Sam Hunt <sam.hunt@npl.co.uk>"
__all__ = []


class QACheckSTACItemGeomCoords(BaseQACheckWorkFlow):
    name = "stac_item_geom_coords"
    version = "1.0"

    def run_check(self, item: dict) -> Tuple[dict, dict]:

