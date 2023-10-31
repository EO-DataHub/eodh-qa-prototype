# eodh_qa_prototype

A prototype implementation of the EODH QA Checker concept.

The aim of this prototype is to illustrate the concept of the QA Checker and its interfaces. It is not intended to define a requirement for how the system should be implemented.

## Installation

Clone the repository, and install from the repository top-level directory with:

``
$ pip install -e .
``

## Structure

The EODH QA Checker should enable the annotation of STAC collections/items in the EODH Catalogue with the results of processes (referred to as QA Check Workflows) intended to verify/validate the quality of datasets. 

Each _QA Check Workflow_ provides the means to check a particular aspect of a collection/item’s quality. Each collection then has a defined set of _QA Check Workflows_ that should run against it at defined time intervals or triggered by defined events – to be handled by the EODH Event and Notification Service (ENS) - this is not implemented in this prototype.

QA check workflows in this prototype are Python classes, which are subclasses of `eodh_qa_prototype.qa_check_workflows.base.BaseQACheckWorkflow`. The example repository of _QA Check Workflows_ in the module `eodh_qa_prototype.qa_check_workflows`. 

Collections are assigned a set of _QA Check Workflows_ to run against the collection as a whole, or individual items in teh collection. In the prototype this is defined by `eodh_qa_prototype/etc/collectionqa.yaml`. 

Assigned QA check workflows are run by the QA Checker Runner. In the prototype this is `eodh_qa_prototype.runner.QACheckRunner` class.


## Example Scripts

Run the illustrative example with:

``
$ python example_scripts/example_workflow.py
``

This runs all the _QA Check Workflows_ assigned to a Sentinel-2 STAC item.