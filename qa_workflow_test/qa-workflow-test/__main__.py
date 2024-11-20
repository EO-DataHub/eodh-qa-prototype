import os
import sys
import datetime as dt
import json
import pystac
from pathlib import Path

import boto3

out_dir = os.getcwd()

def do_func(args):
    # s3 = boto3.client("s3") - not needed?
    s3_endpoint = args[1]

    # set the environment variable for the S3 endpoint, in the future this will be set outside of the code.
    os.environ["AWS_S3_ENDPOINT"] = s3_endpoint

    # name stac item/catalog after qa check
    base_name = 'qa_check_doc_review'

    create_stac_item(base_name)
    create_stac_catalog_root(base_name)


def qa_check_doc_review():
    # maturity matrix as a dict
    maturity_matrix_dict = {
        "product_information":
            {
                "product_details": {"grade": "good", "ref": "https://asdf"},
                "availability_and_accessability": {"grade": "basic", "ref": "https://asdf"},
                "product_format_flags_and_metadata": {"grade": "excellent", "ref": "https://asdf"},
                "...": {"grade": "good", "ref": "https://asdf"}
            },
        "metrology":
            {
                "radiometric_calibration_and_characterisation)": {"grade": "excellent", "ref": "https://asdf"},
                "geometric_calibration_and_characterisation": {"grade": "excellent", "ref": "https://asdf"},
                "metrological_traceability_documentation": {"grade": "basic", "ref": "https://asdf"},
                "...": {"grade": "good", "ref": "https://asdf"}
            },
        "product_generation":
            {
                "radiometric_calibration_algorithm": {"grade": "good", "ref": "https://asdf"},
                "geometric_processing": {"grade": "good", "ref": "https://asdf"},
                "...": {"grade": "good", "ref": "https://asdf"}
            },
    }

    # full result blob
    qa_check_result_output = {
        "data_collection": "Sentinel-2 L1C",
        "check_name": "documentation review",
        "result": maturity_matrix_dict,
        "result_vocab": "vocab/url",
        "check_datetime": dt.datetime.now().strftime("%Y%m%dT%H%M"),
        "check_date_validity_end": (dt.datetime.now() + dt.timedelta(365)).strftime("%Y%m%dT%H%M"),  # approx. 12 months
        "check_author": "S Malone",
        "check_version": "1.0",
        "ref_url": {"documentation_1": "url", "documentation_2": "url", "...": "url"}
    }

    # save to JSON
    qa_check_result_doc_review = json.dumps(qa_check_result_output)

    return qa_check_result_doc_review


def create_stac_item(out_name):
    qa_check_results_dict = json.loads(qa_check_doc_review())
    stem = Path(out_name).stem  # later for "id": f"{stem}-{now}"

    # # create stac item manually
    # STAC_item = pystac.item.Item(
    #     id=qa_check_results_dict["data_collection"].replace(" ", "_")+'_qa_check_test',
    #     geometry=None,
    #     bbox=None,
    #     datetime=qa_check_results_dict["check_datetime"],
    #     # start_datetime=qa_check_results_dict["check_datetime"],
    #     # end_datetime=qa_check_results_dict["check_date_validity_end"],
    #     properties={'full_qa_check_result_output': qa_check_results_dict},
    # )

    data = dict(id = qa_check_results_dict["data_collection"].replace(" ", "_") + '_qa_check_test',
                geometry=None,
                bbox=None,
                datetime=qa_check_results_dict["check_datetime"],
                # start_datetime=qa_check_results_dict["check_datetime"],
                # end_datetime=qa_check_results_dict["check_date_validity_end"],
                properties={'full_qa_check_result_output': qa_check_results_dict}
                )

    with open(f"{out_dir}/{stem}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def create_stac_catalog_root(out_name):
    stem = Path(out_name).stem
    data = {
        "stac_version": "1.0.0",
        "id": "catalog",
        "type": "Catalog",
        "description": "Root catalog",
        "links": [
            {"type": "application/json", "rel": "item", "href": f"{stem}.json"},
            {"type": "application/json", "rel": "self", "href": "catalog.json"},
        ],
    }
    with open(f"{out_dir}/catalog.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    do_func(sys.argv)
