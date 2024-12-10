"""eodh_qa_prototype.qa_check_workflows.absolute_radiometry - validation of L1 radiometry"""

from typing import Tuple
from eodh_qa_prototype.qa_check_workflows.base import BaseQACheckWorkFlow

__author__ = "Sam Hunt <sam.hunt@npl.co.uk>"
__all__ = ["AbsoluteRadiometry"]


class AbsoluteRadiometry(BaseQACheckWorkFlow):
    name = "absolute_radiometry"
    version = "1.0"

    def run_check(self, item: dict) -> Tuple[dict, dict]:
        """
        Checks that absolute radiometry of L1 radiance/reflectance imagery is in spec

        :param item: STAC record for catalogue item
        :return: check result and ancillary info
        """

        pass


if __name__ == "__main__":
    pass
