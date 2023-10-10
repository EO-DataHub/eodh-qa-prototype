"""example_workflow - script to prototype qa check workflow for EODH"""

__author__ = ["Sam Hunt <sam.hunt@npl.co.uk>", "Sam Malone <samantha.malone@npl.co.uk>"]
__all__ = []


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

    return None


if __name__ == "__main__":
    main()
