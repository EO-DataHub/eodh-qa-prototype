"""eodh_qa_prototype.runner - QA service runner"""

import yaml
import os
from typing import List, Tuple
from eodh_qa_prototype.qa_check_workflows import qa_check_workflow_registry

__author__ = "Sam Hunt <sam.hunt@npl.co.uk>"
__all__ = ["QACheckRunner"]

ETC_DIRECTORY = os.path.join(os.path.dirname(__file__), "etc")
COLLECTIONQA_CONFIG_PATH = os.path.join(ETC_DIRECTORY, "collectionqa.yaml")


class QACheckRunner:
    """
    Prototype runner for EODH QA Service

    :param collection_qa_config_path: path to collection qa configuration yaml file
    """

    def __init__(self, collection_qa_config_path: str = COLLECTIONQA_CONFIG_PATH):

        self.collectionqa = None     # configuration of QA check workflows assignment to collections/items

        # if collection qa configuration provided populate attribute
        with open(collection_qa_config_path, 'r') as f:
            self.collectionqa = yaml.safe_load(f)

    def run_item_qa_check_workflows(self, item: dict) -> List[Tuple[dict, dict]]:
        """
        Runs all QA check workflows for input item

        :param item: stac item
        :return: list of return values per qa check workflow run on item (where each qa check workflow return value is a tuple of `result` and `ancillary_info` dictionaries)
        """

        # Get QA check workflows assigned to item

        collection = item["collection"]
        item_qa_check_workflow_names = self.collectionqa[collection]["item_qa_check_workflows"]

        # Run through each QA check workflow

        results = []

        for qa_check_workflow_name in item_qa_check_workflow_names:
            qa_check_workflow = qa_check_workflow_registry[qa_check_workflow_name]()
            result = qa_check_workflow.run_check(item)
            results.append(result)

        return results


if __name__ == "__main__":
    pass
