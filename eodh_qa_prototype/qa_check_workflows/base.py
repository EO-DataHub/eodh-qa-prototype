"""eodh_qa_prototype.qa_check_workflows.base - base class for QA check workflows"""

import abc
from typing import Tuple

__author__ = "Sam Hunt <sam.hunt@npl.co.uk>"
__all__ = ["BaseQACheckWorkFlow"]


class BaseQACheckWorkFlow(abc.ABC):
    """
    Base class for QA Check Workflow implementations
    """

    @property
    @abc.abstractmethod
    def name(self):
        """
        QA check workflow name
        """
        pass

    @property
    @abc.abstractmethod
    def version(self):
        """
        QA check workflow version
        """
        pass

    @abc.abstractmethod
    def run_check(self, item: dict) -> Tuple[dict, dict]:
        """
        Method to run QA check workflow

        :param item: STAC record for catalogue item
        :return: check result and ancillary info
        """

        pass


if __name__ == "__main__":
    pass
