from eodh_qa_prototype.qa_check_workflows.stac_geometry_coordinates import QACheckSTACItemGeomCoords
from eodh_qa_prototype.qa_check_workflows.absolute_radiometry import AbsoluteRadiometry

__all__ = ["qa_check_workflow_registry"]

qa_check_workflow_registry = {
    QACheckSTACItemGeomCoords.name: QACheckSTACItemGeomCoords,
    AbsoluteRadiometry.name: AbsoluteRadiometry
}
