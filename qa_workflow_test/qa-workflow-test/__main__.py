import datetime as dt
import json


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
    # doc_review_save_file = open("qa_check_result_doc_review", "w")
    qa_check_result_doc_review = json.dumps(qa_check_result_output)
    # doc_review_save_file.close()

    return qa_check_result_doc_review


def createStacItem():
    pass


if __name__ == "__main__":
    qa_check_doc_review()
