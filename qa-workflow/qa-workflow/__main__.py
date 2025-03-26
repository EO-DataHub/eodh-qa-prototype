import os
import sys
import datetime as dt
import json
from pathlib import Path
import requests
import xarray as xr
import numpy as np
# import mimetypes

import boto3

out_dir = os.getcwd()


def run_check(args):
    # s3 = boto3.client("s3")  #- not needed?
    s3_endpoint = args[1]
    qa_check_type = args[2]  # 'radiometric_unc'/'doc_review'
    dates = args[3]  # '2022-01-01,2022-12-31' or None (test if can use None or need 'None')
    data_collection = args[4]  # 'planet'

    # get from date range
    if len(dates) > 11:
        dates_list = get_dates_list(dates)

    # set the environment variable for the S3 endpoint, in the future this will be set outside of the code.
    os.environ["AWS_S3_ENDPOINT"] = s3_endpoint

    eodh_coll_rel_dict = {'planet': 'planet_psscene',
                           'airbus_phr': 'airbus_phr',
                           's2a': 'sentinel-2_l1c',
                           's2b': 'sentinel-2_l1c',
                           's2': 'sentinel-2_l1c'}

    eodh_data_coll = eodh_coll_rel_dict[data_collection]

    if qa_check_type == 'radiometric_unc':
        # name stac items & catalog after qa check
        base_name = f'{eodh_data_coll}_qa_check_radiometric_unc'

        # get matchups for that time period
        url = f'http://db-api.eba-3ean8bmb.eu-west-2.elasticbeanstalk.com/matchups?sensor1={data_collection}&sensor2=RCN-GONA&dates={dates}'
        response = requests.get(url)
        mup_dict = json.loads(response.text)
        mup_ds = xr.Dataset.from_dict(mup_dict)

        if mup_ds:
            create_stac_items_rad_unc(data_collection, base_name, mup_ds, dates, dates_list)
            create_stac_collection(base_name, dates_list)
            # create_stac_catalog(base_name)
            create_stac_catalog_root(base_name)
        else:
            return
    elif qa_check_type == 'doc_review':
        # name stac items & catalog after qa check
        base_name = f'{eodh_data_coll}_qa_check_doc_review'
        create_stac_item_doc_review(data_collection, base_name, dates)
        create_stac_collection(base_name, None)
        # create_stac_catalog(base_name)
        create_stac_catalog_root(base_name)


# get dates list from daterange input
def get_dates_list(date_string):  # may need to update if not always doing 1 full year

    if date_string == 'None':
        return None

    year = int(date_string[0:4])
    date_list = []
    for month in range(11):  # up to Nov as Dec would break due to month+2
        date_list.append(dt.datetime(year, month + 1, 1).strftime("%Y-%m-%d")+','+(dt.datetime(year, month + 2, 1) - dt.timedelta(
            1)).strftime("%Y-%m-%d"))
    date_list.append(dt.datetime(year, 12, 1).strftime("%Y-%m-%d")+','+dt.datetime(year, 12, 31).strftime("%Y-%m-%d"))

    return date_list #['2022-01-01,2022-01-31',
            # '2022-02-01,2022-02-28',
            # '2022-03-01,2022-03-31',
            # '2022-04-01,2022-04-30',
            # '2022-05-01,2022-05-31',
            # '2022-06-01,2022-06-30',
            # '2022-07-01,2022-07-31',
            # '2022-08-01,2022-08-31',
            # '2022-09-01,2022-09-30',
            # '2022-10-01,2022-10-31',
            # '2022-11-01,2022-11-30',
            # '2022-12-01,2022-12-31',
            # ]

def qa_check_doc_review(data_collection):
    if data_collection == 'planet':
        matmat = {
            "product_information": {
                "product_details": {
                    "value": "excellent",
                    "links": [
                        {
                            "type": "application/pdf",
                            "href": "https://assets.planet.com/docs/Planet_PSScene_Imagery_Product_Spec_letter_screen.pdf",
                            "title": "PlanetScope Product Specifications, 2023"
                        },
                        {
                            "type": "application/pdf",
                            "href": "https://support.planet.com/hc/en-us/articles/360037649554-L1-Data-Quality-Reports-for-the-PlanetScope-Constellation",
                            "title": "Planet L1 Data Quality Report Superdove 8-Band General Availability, 2021"
                        }
                    ]
                },
                "availability_and_accessability": {
                    "value": "basic",
                    "links": [
                        {
                            "type": "application/pdf",
                            "href": "https://doi.org/10.1038/sdata.2016.18",
                            "title": "Wilkinson, M., Dumontier, M., Aalbersberg, I. et al. The FAIR Guiding Principles for scientific data management and stewardship. Sci Data 3, 160018 (2016)"
                        },
                    ]
                },
                "product_format_flags_and_metadata": {
                    "value": "good",
                    "links": []
                },
                "user_documentation": {
                    "value": "good",
                    "links": [
                        {
                            "type": "application/pdf",
                            "href": "https://assets.planet.com/docs/Planet_PSScene_Imagery_Product_Spec_letter_screen.pdf",
                            "title": "PlanetScope Product Specifications, 2023"
                        },
                        {
                            "type": "application/pdf",
                            "href": "https://developers.planet.com/docs/data/planetscope/",
                            "title": "PlanetScope Overview"
                        }
                    ]
                }
            },
            "metrology":
                {
                    "radiometric_calibration_and_characterisation": {
                        "value": "good",
                        "links": [
                            {
                                "type": "application/pdf",
                                "href": "https://assets.planet.com/docs/radiometric_calibration_white_paper.pdf",
                                "title": "On-Orbit Radiometric Calibration of the Planet Satellite Fleet, Radiometric Calibration White paper, January 2022"
                            }
                        ]
                    },
                    "geometric_calibration_and_characterisation": {
                        "value": "good",
                        "links": [
                            {
                                "type": "application/pdf",
                                "href": "https://assets.planet.com/docs/Planet_PSScene_Imagery_Product_Spec_June_2021.pdf",
                                "title": "PlanetScope Product Specifications, PSScene Imagery Product Spec FINAL | June 2021, June 2021"
                            }
                        ]
                    },
                    "metrological_traceability_documentation": {
                        "value": "not assessable",
                        "links": []
                    },
                    "uncertainty_characterisation": {
                        "value": "basic",
                        "links": [
                            {
                                "type": "application/pdf",
                                "href": "https://support.planet.com/hc/en-us/articles/360037649554-L1-Data-Quality-Reports-for-the-PlanetScope-Constellation",
                                "title": "Planet L1 Data Quality Report Superdove 8-Band General Availability, 2021"
                            }
                        ]
                    },
                    "ancillary_data": {
                        "value": "basic",
                        "links": [
                            {
                                "type": "application/pdf",
                                "href": "https://support.planet.com/hc/en-us/articles/360037649554-L1-Data-Quality-Reports-for-the-PlanetScope-Constellation",
                                "title": "Planet L1 Data Quality Report Superdove 8-Band General Availability, 2021"
                            }
                        ]
                    }
                },
            "product_generation":
                {
                    "calibration_algorithm": {
                        "value": "good",
                        "links": [
                            {
                                "type": "application/pdf",
                                "href": "https://assets.planet.com/docs/radiometric_calibration_white_paper.pdf",
                                "title": "On-Orbit Radiometric Calibration of the Planet Satellite Fleet, Radiometric Calibration White paper, January 2022"
                            },
                            {
                                "type": "application/pdf",
                                "href": "https://assets.planet.com/docs/Planet_PSScene_Imagery_Product_Spec_June_2021.pdf",
                                "title": "Planet Imagery Product Specifications : combined-imagery-product-spec-final-august-2019.pdf, August 2019"
                            }
                        ]
                    },
                    "geometric_processing": {
                        "value": "good",
                        "links": [
                            {
                                "type": "application/pdf",
                                "href": "https://assets.planet.com/docs/Planet_PSScene_Imagery_Product_Spec_June_2021.pdf",
                                "title": "Planet Imagery Product Specifications : combined-imagery-product-spec-final-august-2019.pdf, August 2019"
                            }
                        ]
                    },
                    "retrieval_algorithm": {
                        "value": "not assessed",
                        "links": []
                    },
                    "mission_specific_processing": {
                        "value": "not assessed",
                        "links": []
                    },
                }
        }
    elif data_collection == 'airbus_phr':
        matmat = {
            "product_information": {
                "product_details": {
                    "value": "excellent",
                    "links": [
                        {
                            "type": "application/pdf",
                            "href": "https://storage.googleapis.com/p-oaf-ibe-back-00e-strapi-uploads/210415_Airbus_Pleiades_Imagery_user_guide_be12b8f35b/210415_Airbus_Pleiades_Imagery_user_guide_be12b8f35b.pdf",
                            "title": "Airbus Pléiades Imagery User Guide. (Report Number: USRPHR-DT-125-SPOT-2.0, Date of issue: October, 18, 2012)"
                        },
                    ]
                },
                "availability_and_accessability": {
                    "value": "basic",
                    "links": [
                        {
                            "type": "application/pdf",
                            "href": "https://doi.org/10.1038/sdata.2016.18",
                            "title": "Wilkinson, M., Dumontier, M., Aalbersberg, I. et al. The FAIR Guiding Principles for scientific data management and stewardship. Sci Data 3, 160018 (2016)"
                        },
                    ]
                },
                "product_format_flags_and_metadata": {
                    "value": "good",
                    "links": [
                        {
                            "type": "application/pdf",
                            "href": "https://storage.googleapis.com/p-oaf-ibe-back-00e-strapi-uploads/210415_Airbus_Pleiades_Imagery_user_guide_be12b8f35b/210415_Airbus_Pleiades_Imagery_user_guide_be12b8f35b.pdf",
                            "title": "Airbus Pléiades Imagery User Guide. (Report Number: USRPHR-DT-125-SPOT-2.0, Date of issue: October, 18, 2012)"
                        },
                    ]
                },
                "user_documentation": {
                    "value": "good",
                    "links": [
                        {
                            "type": "application/pdf",
                            "href": "https://storage.googleapis.com/p-oaf-ibe-back-00e-strapi-uploads/210415_Airbus_Pleiades_Imagery_user_guide_be12b8f35b/210415_Airbus_Pleiades_Imagery_user_guide_be12b8f35b.pdf",
                            "title": "Airbus Pléiades Imagery User Guide. (Report Number: USRPHR-DT-125-SPOT-2.0, Date of issue: October, 18, 2012)"
                        },
                    ]
                }
            },
            "metrology":
                {
                    "radiometric_calibration_and_characterisation": {
                        "value": "basic",
                        "links": [
                            {
                                "type": "application/pdf",
                                "href": "https://storage.googleapis.com/p-oaf-ibe-back-00e-strapi-uploads/210415_Airbus_Pleiades_Imagery_user_guide_be12b8f35b/210415_Airbus_Pleiades_Imagery_user_guide_be12b8f35b.pdf",
                                "title": "Airbus Pléiades Imagery User Guide. (Report Number: USRPHR-DT-125-SPOT-2.0, Date of issue: October, 18, 2012)"
                            },
                        ]
                    },
                    "geometric_calibration_and_characterisation": {
                        "value": "basic",
                        "links": [
                            {
                                "type": "application/pdf",
                                "href": "https://storage.googleapis.com/p-oaf-ibe-back-00e-strapi-uploads/210415_Airbus_Pleiades_Imagery_user_guide_be12b8f35b/210415_Airbus_Pleiades_Imagery_user_guide_be12b8f35b.pdf",
                                "title": "Airbus Pléiades Imagery User Guide. (Report Number: USRPHR-DT-125-SPOT-2.0, Date of issue: October, 18, 2012)"
                            },
                        ]
                    },
                    "metrological_traceability_documentation": {
                        "value": "not assessable",
                        "links": []
                    },
                    "uncertainty_characterisation": {
                        "value": "not assessable",
                        "links": []
                    },
                    "ancillary_data": {
                        "value": "good",
                        "links": [
                            {
                                "type": "application/pdf",
                                "href": "https://storage.googleapis.com/p-oaf-ibe-back-00e-strapi-uploads/210415_Airbus_Pleiades_Imagery_user_guide_be12b8f35b/210415_Airbus_Pleiades_Imagery_user_guide_be12b8f35b.pdf",
                                "title": "Airbus Pléiades Imagery User Guide. (Report Number: USRPHR-DT-125-SPOT-2.0, Date of issue: October, 18, 2012)"
                            },
                        ]
                    }
                },
            "product_generation":
                {
                    "calibration_algorithm": {
                        "value": "not assessable",
                        "links": [
                            {
                                "type": "application/pdf",
                                "href": "https://doi.org/10.1117/12.2023337",
                                "title": f"Latry, Laurent Lebegue, Florie Lenoir, Florence Porez-Nadal. PLEIADES-HR 1A&1B image quality commissioning: innovative radiometric calibration methods and results, Proc. SPIE 8866, Earth Observing Systems XVIII, 886610 (23 September 2013)"
                            },
                        ]
                    },
                    "geometric_processing": {
                        "value": "not assessable",
                        "links": []
                    },
                    "retrieval_algorithm": {
                        "value": "not assessed",
                        "links": []
                    },
                    "mission_specific_processing": {
                        "value": "not assessed",
                        "links": []
                    },
                }
        }
    elif data_collection in ['s2', 's2a', 's2b']:
        matmat = {
            "product_information": {
                "product_details": {
                    "value": "ideal",
                    "links": [
                        {
                            "type": "application/pdf",
                            "href": "https://sentiwiki.copernicus.eu/web/sentinel-2",
                            "title": "SentiWiki"
                        },
                    ]
                },
                "availability_and_accessability": {
                    "value": "ideal",
                    "links": [
                        {
                            "type": "application/pdf",
                            "href": "https://doi.org/10.1038/sdata.2016.18",
                            "title": "Wilkinson, M., Dumontier, M., Aalbersberg, I. et al. The FAIR Guiding Principles for scientific data management and stewardship. Sci Data 3, 160018 (2016)"
                        },
                    ]
                },
                "product_format_flags_and_metadata": {
                    "value": "ideal",
                    "links": [
                        {
                            "type": "application/pdf",
                            "href": "https://sentiwiki.copernicus.eu/__attachments/1692737/S2-PDGS-CS-DI-PSD%20-%20S2%20Product%20Specification%20Document%202024%20-%2015.0.pdf?inst-v=31732265-f315-437d-93c5-06068d410876",
                            "title": "CS team Sentinel-2 Product Specification Document v15, S2-PDGS-CS-DI-PSD, 2024."
                        },
                        {
                            "type": "application/pdf",
                            "href": "https://ceos.org/ard/files/Self%20Assessments/SR/v5.0/WGCV_CARD4L_Evaluation_for_ESA-S2_SR_at_Threshold_PFS_v5.pdf",
                            "title": "ESA CARD4L self-assessment of Sentinel-2 Surface Reflectance PFS v5"
                        },
                    ]
                },
                "user_documentation": {
                    "value": "ideal",
                    "links": [
                        {
                            "type": "application/pdf",
                            "href": "https://sentiwiki.copernicus.eu/web/sentinel-2",
                            "title": "SentiWiki"
                        },
                        {
                            "type": "application/pdf",
                            "href": "https://sentiwiki.copernicus.eu/__attachments/1692737/S2-PDGS-MPC-ATBD-L1%20-%20Sentinel-2%20Level%201%20Algorithm%20Theoretical%20Bases%20Document%202023%20-%201.1.pdf?inst-v=31732265-f315-437d-93c5-06068d410876",
                            "title": "S2-MPC, Level-1 Algorithm Theoretical Basis Document v1.1, S2-PDGS-MPC_ATBD-L1_V1.1, 2023."
                        },
                        {
                            "type": "application/pdf",
                            "href": "https://sentiwiki.copernicus.eu/__attachments/1692737/S2-PDGS-CS-DI-PSD%20-%20S2%20Product%20Specification%20Document%202024%20-%2015.0.pdf?inst-v=31732265-f315-437d-93c5-06068d410876",
                            "title": "CS team Sentinel-2 Product Specification Document v15, S2-PDGS-CS-DI-PSD, 2024."
                        },
                    ]
                }
            },
            "metrology":
                {
                    "radiometric_calibration_and_characterisation": {
                        "value": "excellent",
                        "links": [
                            {
                                "type": "application/pdf",
                                "href": "https://doi.org/10.1117/12.2028854",
                                "title": "E. Mazy, et al. Sentinel-2 diffuser on-ground calibration, Proc. SPIE 8889, Sensors, Systems, and Next-Generation Satellites XVII, 88890W (24 October 2013)"
                            },
                            {
                                "type": "application/pdf",
                                "href": "https://sentiwiki.copernicus.eu/__attachments/1673423/OMPC.CS.DQR.001.12-2024%20-%20MSI%20L1C%20DQR%20January%202025%20-%20107.0.pdf?inst-v=31732265-f315-437d-93c5-06068d410876",
                                "title": "OPT-MPC, Data Quality Report Sentinel-2 MSI L1C January 2025, OMPC.CS.DQR.002.12-2024, 2025."
                            },
                            {
                                "type": "application/pdf",
                                "href": "https://doi.org/10.3390/rs11202401",
                                "title": "Bouvet, M. et al. RadCalNet: A Radiometric Calibration Network for Earth Observing Imagers Operating in the Visible to Shortwave Infrared Spectral Range. Remote Sens. 2019, 11, 2401."
                            },
                            {
                                "type": "application/pdf",
                                "href": "https://doi.org/10.1016/j.rse.2019.111369",
                                "title": "Lamquin, N. et al. (2019). An inter-comparison exercise of Sentinel-2 radiometric validations assessed by independent expert groups. Remote Sens. of Env. 2019, 233, 111369."
                            }
                        ]
                    },
                    "geometric_calibration_and_characterisation": {
                        "value": "excellent",
                        "links": [
                            {
                                "type": "application/pdf",
                                "href": "https://sentiwiki.copernicus.eu/__attachments/1673423/OMPC.CS.DQR.001.12-2024%20-%20MSI%20L1C%20DQR%20January%202025%20-%20107.0.pdf?inst-v=31732265-f315-437d-93c5-06068d410876",
                                "title": "OPT-MPC, Data Quality Report Sentinel-2 MSI L1C January 2025, OMPC.CS.DQR.002.12-2024, 2025."
                            },
                            {
                                "type": "application/pdf",
                                "href": "https://sentiwiki.copernicus.eu/__attachments/1692737/S2-MPC_PHB_GCP_L1B_L1C_GRI_V3.pdf?inst-v=31732265-f315-437d-93c5-06068d410876",
                                "title": "S2-MPC, Copernicus Sentinel-2 GRI as Database of GCPs in L1B & L1C - Product Handbook v3, S2-MPC_PHB_GCP_L1B_L1C_GRI, 2023."
                            },
                            {
                                "type": "application/pdf",
                                "href": "https://sentiwiki.copernicus.eu/__attachments/1692737/S2-MPC_VAL_GCP_L1B_L1C_GRI_V3.pdf?inst-v=31732265-f315-437d-93c5-06068d410876",
                                "title": "S2-MPC, Copernicus Sentinel-2 GRI as Database of GCPs in L1B & L1C - Validation Report, S2-MPC_VAL_GCP_L1B_L1C_GRI, 2023"
                            },
                        ]
                    },
                    "metrological_traceability_documentation": {
                        "value": "excellent",
                        "links": [
                            {
                                "type": "application/pdf",
                                "href": "https://doi.org/10.1117/12.2028854",
                                "title": "E. Mazy, et al. Sentinel-2 diffuser on-ground calibration, Proc. SPIE 8889, Sensors, Systems, and Next-Generation Satellites XVII, 88890W (24 October 2013)"
                            },
                            {
                                "type": "application/pdf",
                                "href": "https://sentiwiki.copernicus.eu/__attachments/1673423/OMPC.CS.DQR.001.12-2024%20-%20MSI%20L1C%20DQR%20January%202025%20-%20107.0.pdf?inst-v=31732265-f315-437d-93c5-06068d410876",
                                "title": "OPT-MPC, Data Quality Report Sentinel-2 MSI L1C January 2025, OMPC.CS.DQR.002.12-2024, 2025."
                            },
                        ]
                    },
                    "uncertainty_characterisation": {
                        "value": "excellent",
                        "links": [
                            {
                                "type": "application/pdf",
                                "href": "https://doi.org/10.3390/rs9020178",
                                "title": "Gorroño, J. et al., A Radiometric Uncertainty Tool for the Sentinel 2 Mission. Remote Sens. 2017, 9, 178."
                            },
                            {
                                "type": "application/pdf",
                                "href": "https://doi.org/10.1080/22797254.2018.1471739",
                                "title": "Gorroño, J.,et al. (2018). Providing uncertainty estimates of the Sentinel-2 top-of-atmosphere measurements for radiometric validation activities. European Journal of Remote Sensing, 51(1), 650–666."
                            }
                        ]
                    },
                    "ancillary_data": {
                        "value": "excellent",
                        "links": [
                            {
                                "type": "application/pdf",
                                "href": "https://sentiwiki.copernicus.eu/__attachments/1692737/S2-MPC_PHB_GCP_L1B_L1C_GRI_V3.pdf?inst-v=31732265-f315-437d-93c5-06068d410876",
                                "title": "S2-MPC, Copernicus Sentinel-2 GRI as Database of GCPs in L1B & L1C - Product Handbook v3, S2-MPC_PHB_GCP_L1B_L1C_GRI, 2023."
                            },
                            {
                                "type": "application/pdf",
                                "href": "https://s3.waw3-1.cloudferro.com/swift/v1/portal_uploads_prod/GEO1988-CopernicusDEM-RP-001_ValidationReport_I3.0_08.2024.pdf",
                                "title": "Vera Leister-Taylor, Copernicus Digital Elevation Model Validation Report v3, GEO.2018-1988-2, 2020."
                            },
                        ]
                    }
                },
            "product_generation":
                {
                    "calibration_algorithm": {
                        "value": "ideal",
                        "links": [
                            {
                                "type": "application/pdf",
                                "href": "https://sentiwiki.copernicus.eu/__attachments/1692737/S2-PDGS-MPC-ATBD-L1%20-%20Sentinel-2%20Level%201%20Algorithm%20Theoretical%20Bases%20Document%202023%20-%201.1.pdf?inst-v=31732265-f315-437d-93c5-06068d410876",
                                "title": "S2-MPC, Level-1 Algorithm Theoretical Basis Document v1.1, S2-PDGS-MPC_ATBD-L1_V1.1, 2023."
                            },
                        ]
                    },
                    "geometric_processing": {
                        "value": "ideal",
                        "links": [
                            {
                                "type": "application/pdf",
                                "href": "https://sentiwiki.copernicus.eu/__attachments/1692737/S2-PDGS-MPC-ATBD-L1%20-%20Sentinel-2%20Level%201%20Algorithm%20Theoretical%20Bases%20Document%202023%20-%201.1.pdf?inst-v=31732265-f315-437d-93c5-06068d410876",
                                "title": "S2-MPC, Level-1 Algorithm Theoretical Basis Document v1.1, S2-PDGS-MPC_ATBD-L1_V1.1, 2023."
                            },
                        ]
                    },
                    "retrieval_algorithm": {
                        "value": "not assessed",
                        "links": []
                    },
                    "mission_specific_processing": {
                        "value": "ideal",
                        "links": [
                            {
                                "type": "application/pdf",
                                "href": "https://sentiwiki.copernicus.eu/__attachments/1692737/S2-PDGS-MPC-ATBD-L1%20-%20Sentinel-2%20Level%201%20Algorithm%20Theoretical%20Bases%20Document%202023%20-%201.1.pdf?inst-v=31732265-f315-437d-93c5-06068d410876",
                                "title": "S2-MPC, Level-1 Algorithm Theoretical Basis Document v1.1, S2-PDGS-MPC_ATBD-L1_V1.1, 2023."
                            },
                        ]
                    },
                }
        }
    return matmat

def create_stac_item_doc_review(data_collection, out_name, review_date):
    stem = Path(out_name).stem  # later for "id": f"{stem}-{now}"
    # size = os.path.getsize(f"{out_name}")
    # mime = mimetypes.guess_type(f"{out_name}")[0]
    root_catalog_name = '_'.join(stem.split('_')[0:3])
    qa_check_results_dict = qa_check_doc_review(data_collection)

    # dump qa result json file
    with open(f"{out_dir}/output_{stem}.json", "w", encoding="utf-8") as f:
        json.dump(qa_check_results_dict, f, ensure_ascii=False, indent=4)

    item_data = dict(id=f"{stem}",
                     type="Feature",
                     stac_version="1.0.0",
                     geometry= None, #{  # null coords
                         # "type": "Point",
                         # "coordinates":[0, 0],
                     #},
                    # bbox=[15.10274, -23.60723694, 15.13462891, -23.59451068],
                     properties={"datetime": dt.datetime.strptime(review_date,"%Y-%m-%d").strftime("%Y%m%dT%H%M%S.%f"),
                                 },
                     links=[
                         {"type": "application/geo+json", "rel": "self", "href": f"{stem}.json"},
                         {"type": "application/json", "rel": "collection", "href": "qa_documentation.json"},
                         {"type": "application/json", "rel": "root", "href": "catalog.json"},
                     ],
                     assets={
                         f"{stem}": {
                             # "type": f"{mime}",
                             # "file:size": size,
                             "roles": ["data"],
                             "href": f"{out_name}",
                         },
                         f"qa-outputs": {
                             "href": f"output_{stem}.json",
                             "title": f"output_{stem}.json",
                             "description": f"QA documentation review output for {stem}",
                             "type": "application/json",
                             # "roles": ["data"],
                         },
                     },
                     )

    with open(f"{out_dir}/{stem}.json", "w", encoding="utf-8") as f:
        json.dump(item_data, f, ensure_ascii=False, indent=4)


def qa_check_rad_val(data_collection, out_name, mup_ds, date_range):

    dates = [date_range.split(',')[0], date_range.split(',')[1]]
    datetimes_range = [dt.datetime.strptime(dates[0], "%Y-%m-%d"), dt.datetime.strptime(dates[1], "%Y-%m-%d")]

    # remove nan values
    del_list_idx = []
    for j, arr in enumerate(mup_ds[f'{data_collection}_RCN-GONA_BiasVals'].values):
        if all(arr[i] == -9999 for i in range(13)):
            del_list_idx.append(j)

    mup_ds_bias_vals = np.delete(mup_ds[f'{data_collection}_RCN-GONA_BiasVals'].values, del_list_idx, axis=0)
    # mup_ds_bias_unc_vals = np.delete(mup_ds[f'{data_collection_RCN-GONA_BiasUncVals'].values, del_list_idx, axis=0)
    mup_ds_rcn_meas_vals = np.delete(mup_ds[f'{data_collection}_RCN-GONA_MeasValsSensor2'].values, del_list_idx, axis=0)
    mup_ds_rcn_meas_unc_vals = np.delete(mup_ds[f'{data_collection}_RCN-GONA_MeasUncValsSensor2'].values, del_list_idx, axis=0)

    bias_vals = np.ones(mup_ds_bias_vals.transpose().shape) * np.nan  # shape (13, 228)
    bias_unc_vals = np.ones(mup_ds_bias_vals.transpose().shape) * np.nan  # (13, 228)
    rcn_meas_vals = np.ones(mup_ds_bias_vals.transpose().shape) * np.nan  # (13, 228)
    rcn_meas_unc_vals = np.ones(mup_ds_bias_vals.transpose().shape) * np.nan  # (13, 228)

    # reorder vals
    for k in range(bias_vals.shape[1]):  # ~228 matchups
        for j in range(bias_vals.shape[0]):  # 13 bands
            bias_vals[j][k] = mup_ds_bias_vals[k][j]
            # bias_unc_vals[j][k] = mup_ds_bias_unc_vals[k][j]
            rcn_meas_vals[j][k] = mup_ds_rcn_meas_vals[k][j]
            rcn_meas_unc_vals[j][k] = mup_ds_rcn_meas_unc_vals[k][j]

    if 'planet' in out_name:
        # first keep only 8 bands for planet
        bias_vals = bias_vals[:8]
        # bias_unc_vals = bias_unc_vals[:8]
        rcn_meas_vals = rcn_meas_vals[:8]
        rcn_meas_unc_vals = rcn_meas_unc_vals[:8]  #np.ones(rcn_meas_vals.shape) * 0.9

        sat_mean_unc = np.array([8.013, 6.798, 6.244, 5.636, 5.771, 6.277, 8.736, 9.229])
        stated_value = ["8.0% (coastal blue)", "6.8% (blue)", "6.2% (green_i)", "5.6% (green_ii)", "5.8% (yellow)", "6.3% (red)", "8.7% (red edge)", "9.2% (NIR)"],  # abs rad unc from doc: https://support.planet.com/hc/en-us/article_attachments/4403255608849 (log in here https://support.planet.com/hc/en-us/articles/360037649554-L1-Data-Quality-Reports-for-the-PlanetScope-Constellation)
        rad_unc_report_title = "PLANET L1 DATA QUALITY REPORT, SUPERDOVE 8-BAND GENERAL AVAILABILITY: Status of Calibration and Data Quality for the SuperDove 8-Band GA, 15/06/21"
        rad_unc_report_ref = "https://support.planet.com/hc/en-us/articles/360037649554-L1-Data-Quality-Reports-for-the-PlanetScope-Constellation"
        sat_checked = "planet"
        eodh_data_coll = 'PSScene'
        doi ="https://staging.eodatahub.org.uk/api/catalogue/stac/catalogs/supported-datasets/catalogs/planet/collections/PSScene"
    elif 'airbus_phr' in out_name:
        # first keep only 4 bands for airbus_phr
        bias_vals = bias_vals[:4]
        # bias_unc_vals = bias_unc_vals[:4]
        rcn_meas_vals = rcn_meas_vals[:4]
        rcn_meas_unc_vals = rcn_meas_unc_vals[:4]  #np.ones(rcn_meas_vals.shape) * 0.9

        sat_mean_unc = np.ones(4) * 5
        stated_value = ["5% (blue)", "5% (green)", "5% (red)", "5% (NIR)"]
        rad_unc_report_title = "PleiadesUserGuide-18072019.pdf"
        rad_unc_report_ref = "https://www.intelligence-airbusds.com/en/8718-user-guides"
        sat_checked = "airbus_phr"
        eodh_data_coll = "Airbus_Pleiades"
        doi = "https://staging.eodatahub.org.uk/api/catalogue/stac/catalogs/supported-datasets/catalogs/airbus/collections/airbus_phr_data"
    elif 'sentinel-2' in out_name:  # or sentinel2
        sat_mean_unc = np.ones(13) * 5
        stated_value = ["5% (B1)", "5% (B2)", "5% (B3)", "5% (B4)","5% (B5)", "5% (B6)", "5% (B7)", "5% (B8)","5% (B9)", "5% (B10)", "5% (B11)", "5% (B12)", "5% (B8A)"]
        rad_unc_report_title = "Data Quality Report Sentinel-2 L1C MSI January 2023"
        rad_unc_report_ref = "https://sentinel.esa.int/documents/247904/4868341/OMPC.CS.DQR.001.12-2022+-+i83r0+-+MSI+L1C+DQR+January+2023.pdf"
        sat_checked = "s2a" #or s2b - todo: update dashboard to accept s2 so can keep s2 in general here
        eodh_data_coll = "Sentinel-2_L1C"
        doi = "https://staging.eodatahub.org.uk/api/catalogue/stac/catalogs/supported-datasets/catalogs/ceda-stac-catalogue/collections/sentinel2_ard"

    rcn_bias_vals_mean = np.ones(len(bias_vals)) * np.nan
    rcn_refl_vals_mean_unc = np.ones(len(bias_vals)) * np.nan

    for k in range(len(bias_vals)):
        rcn_bias_vals_mean[k] = round(sum(bias_vals[k]) / len(bias_vals[k]), 2)
        rcn_refl_vals_mean_unc[k] = round(sum(rcn_meas_unc_vals[k]) / len(rcn_meas_unc_vals[k]), 2)

    comp_unc_vals = np.ones(len(sat_mean_unc)) * 2

    total_unc = np.sqrt(
        sat_mean_unc ** 2 + rcn_refl_vals_mean_unc ** 2 + comp_unc_vals ** 2)  # total unc combines unc from sat product, unc from RCN product, unc from comparison

    # calc E
    e_val = rcn_bias_vals_mean / total_unc

    bands_result_list = []
    for val in range(len(rcn_bias_vals_mean)):
        if abs(e_val[val]) <= 1:
            bands_result_list.append('pass')
        elif abs(e_val[val]) <= 2:
            bands_result_list.append('partial')
        else:  # if >2
            bands_result_list.append('fail')

    if all([bands_result_list[i] == 'pass' for i in range(len(bands_result_list))]):
        overall_result = 'pass'
    elif all([bands_result_list[i] == 'fail' for i in range(len(bands_result_list))]):
        overall_result = 'fail'
    else:
        overall_result = 'partial pass'

    qa_radiometric_check_result_output = {  # output dict of radiometric test result
        "data_collection": eodh_data_coll,
        "data_id_field": doi,
        "uuid": "uuid",
        "check_name": "radiometric uncertainty",
        "results": {
            'data validation': {
                'radiometric uncertainty': {
                    "metric": "https://eodatahub.org.uk/api/ontologies/qa/metrics/data-validation/radiometric-uncertainty",
                    "value": [overall_result, bands_result_list],
                    "stated_value": stated_value,
                    "links": [
                        {"rel": "https://eodatahub.org.uk/api/ontologies/qa/detailed-result-report",
                         "type": "application/pdf",
                         "href": "https://npl-qa-workspace.eodatahub-worksapces.org.uk/files/qa-reports/detailed-report.pdf",  # todo: which report is this?
                         "title": "Detailed QA Check Report for radiometric uncertainty"
                         },
                        {"rel": "https://eodatahub.org.uk/api/ontologies/qa/data_product_report",
                         "type": "application/pdf",
                         "href": rad_unc_report_ref,
                         "title": rad_unc_report_title,
                         },
                        {"rel": "https://eodatahub.org.uk/api/ontologies/qa/data-visualisation",
                         "type": "application/pdf",
                         "href": f"http://ceos-dashboard.eba-krpcapwh.eu-west-2.elasticbeanstalk.com/ceos-dashboard?sat={sat_checked}&refs=RCN-GONA&bands=490,565,665&date={date_range}",
                         "title": "Dashboard displaying detailed QA information for the radiometric uncertainty check"
                         }
                    ],
                }
            }
        },
        "result_vocab": "vocab/url",
        # url to a dict that defines pass/fail/partial etc - different for different test types
        "check_datetime": dt.datetime.now().strftime("%Y%m%dT%H%M%S.%f"),  # now (when check was run)
        "check_datetime_validity_start": datetimes_range[0].strftime("%Y%m%dT%H%M%S.%f"),
        "check_datetime_validity_end": datetimes_range[1].strftime("%Y%m%dT%H%M%S.%f"),
        "check_creator": 'S Malone',
        "contact_point": 'samantha.malone@npl.co.uk',
        "publisher": 'Climate and Earth Observation Group, National Physical Laboratory',
        "eodh_qa_check_version": 1.0,
    }

    return qa_radiometric_check_result_output


def create_stac_items_rad_unc(data_collection, out_name, mup_ds, daterange, dates_list):
    stem = Path(out_name).stem  # later for "id": f"{stem}-{now}"
    # size = os.path.getsize(f"{out_name}")
    # mime = mimetypes.guess_type(f"{out_name}")[0]
    root_catalog_name = '_'.join(stem.split('_')[0:3])

    for dates in dates_list:
        qa_check_results_dict = qa_check_rad_val(data_collection, out_name, mup_ds, dates)

        # dump qa result json file
        with open(f"{out_dir}/output_{stem}_{dates.replace(',', '_')}.json", "w", encoding="utf-8") as f:
            json.dump(qa_check_results_dict, f, ensure_ascii=False, indent=4)

        item_data = dict(id = f"{stem}_{dates.replace(',', '_')}", #qa_check_results_dict["data_collection"].replace(" ", "_") + '_qa_check_test',
                    type = "Feature",
                    stac_version = "1.0.0",
                    geometry = None,
                    # geometry={  # GONA coords
                    #     "type": "Polygon",
                    #     "coordinates": [
                    #         [[15.10274,-23.60723694],
                    #          [15.13462891,-23.60723694],
                    #          [15.13462891,-23.59451068],
                    #          [15.10274,-23.59451068],
                    #          [15.10274,-23.60723694]]
                    #     ],
                    # },
                    # bbox=[15.10274,-23.60723694, 15.13462891,-23.59451068],  # GONA coords
                    properties={"datetime": qa_check_results_dict["check_datetime"],
                                "check_validity_start_datetime": qa_check_results_dict["check_datetime_validity_start"],
                                "check_validity_end_datetime": qa_check_results_dict["check_datetime_validity_end"]
                                },
                    links = [
                        {"type": "application/geo+json", "rel": "self",  "href": f"{stem}_{dates.replace(',', '_')}.json"},
                        {"type": "application/json", "rel": "collection", "href": "qa_radiometric.json"}, # catalog #f"qa_radiometric.json"}
                        {"type": "application/json", "rel": "root", "href": "catalog.json"}, # catalog  #f"{stem}_catalog_{daterange.replace(',', '_')}
                    ],
                    assets = {
                        f"{stem}": {
                            # "type": f"{mime}",
                            # "file:size": size,
                            "roles": ["data"],
                            "href": f"{out_name}",
                        },
                        f"qa-outputs": {
                            "href": f"output_{stem}_{dates.replace(',', '_')}.json",
                            "title": f"output_{stem}_{dates.replace(',', '_')}.json",
                            "description": f"QA radiometric uncertainty results output for {stem}_{dates.replace(',', '_')}",
                            "type": "application/json",
                            # "roles": ["data"],
                        },
                    },
                    )

        with open(f"{out_dir}/{stem}_{dates.replace(',', '_')}.json", "w", encoding="utf-8") as f:
            json.dump(item_data, f, ensure_ascii=False, indent=4)

def create_stac_collection(out_name, dates_list):
    stem = Path(out_name).stem
    root_catalog_name = '_'.join(stem.split('_')[0:3])

    if 'doc_review' in out_name:
        collection_data = {
            "stac_version": "1.0.0",
            "id": f"qa_documentation",
            "type": "Collection",
            "description": "Collection for radiometric QA checks",
            "license": "other",
            "extent": {
                "spatial": {"bbox": [[-180.0, -90.0, 180.0, 90.0]]},
                "temporal": {
                    "interval": [[None, None]]}
            },
            "links": [
                {"type": "application/geo+json", "rel": "item", "href": f"{stem}.json"},
                {"type": "application/json", "rel": "root", "href": "catalog.json"},
                {"type": "application/json", "rel": "parent", "href": "catalog.json"}, #f"{root_catalog_name}.json
                {"type": "application/json", "rel": "self", "href": "qa_documentation.json"},
            ],
        }
        with open(f"{out_dir}/qa_documentation.json", "w", encoding="utf-8") as f:
            json.dump(collection_data, f, ensure_ascii=False, indent=4)

    elif 'radiometric_unc' in out_name:
        collection_data = {
            "stac_version": "1.0.0",
            "id": f"qa_radiometric",
            "type": "Collection",
            "description": "Collection for radiometric QA checks",
            "license": "other",
            "extent": {
                "spatial": {"bbox": [[-180.0, -90.0, 180.0, 90.0]]},
                "temporal": {
                    "interval": [[None, None]]}
            },
            "links": [
                {"type": "application/geo+json", "rel": "item", "href": f"{stem}_{dates_list[0].replace(',', '_')}.json"},
                {"type": "application/geo+json", "rel": "item", "href": f"{stem}_{dates_list[1].replace(',', '_')}.json"},
                {"type": "application/geo+json", "rel": "item", "href": f"{stem}_{dates_list[1].replace(',', '_')}.json"},
                {"type": "application/geo+json", "rel": "item", "href": f"{stem}_{dates_list[3].replace(',', '_')}.json"},
                {"type": "application/geo+json", "rel": "item", "href": f"{stem}_{dates_list[4].replace(',', '_')}.json"},
                {"type": "application/geo+json", "rel": "item", "href": f"{stem}_{dates_list[5].replace(',', '_')}.json"},
                {"type": "application/geo+json", "rel": "item", "href": f"{stem}_{dates_list[6].replace(',', '_')}.json"},
                {"type": "application/geo+json", "rel": "item", "href": f"{stem}_{dates_list[7].replace(',', '_')}.json"},
                {"type": "application/geo+json", "rel": "item", "href": f"{stem}_{dates_list[8].replace(',', '_')}.json"},
                {"type": "application/geo+json", "rel": "item", "href": f"{stem}_{dates_list[9].replace(',', '_')}.json"},
                {"type": "application/geo+json", "rel": "item", "href": f"{stem}_{dates_list[10].replace(',', '_')}.json"},
                {"type": "application/geo+json", "rel": "item", "href": f"{stem}_{dates_list[11].replace(',', '_')}.json"},
                {"type": "application/json", "rel": "root", "href": "catalog.json"}, # catalog  #f"{stem}_catalog_{daterange.replace(',', '_')}
                {"type": "application/json", "rel": "parent", "href": "catalog.json"}, # catalog  # f"{stem}_catalog_{daterange.replace(',', '_')}
                {"type": "application/json", "rel": "self", "href": "qa_radiometric.json"},
            ],
        }
        with open(f"{out_dir}/qa_radiometric.json", "w", encoding="utf-8") as f:
            json.dump(collection_data, f, ensure_ascii=False, indent=4)

# def create_stac_catalog(out_name):
#     stem = Path(out_name).stem
#     root_catalog_name = '_'.join(stem.split('_')[0:3])
#     coll_checked = '_'.join(stem.split('_')[0:2])
#     if 'doc_review' in out_name:
#         collection_name = 'qa_documentation'
#     elif 'radiometric_unc' in out_name:
#         collection_name = 'qa_radiometric'
#     # if 'doc_review' in out_name:
#     catalog_data = {
#         "stac_version": "1.0.0",
#         "id": f"{root_catalog_name}",  # catalog_name #f"{stem}_catalog_{daterange.replace(',', '_')}
#         "type": "Catalog",
#         "description": f"Root catalog for {coll_checked} QA checks",
#         "links": [
#             {"type": "application/json", "rel": "root", "href": "catalog.json"},
#             {"type": "application/json", "rel": "parent", "href": "catalog.json"},
#             {"type": "application/json", "rel": "self", "href": f"{root_catalog_name}.json"},
#             {"type": "application/json", "rel": "child", "href": f"{collection_name}.json"},
#         ],
#     }
#     with open(f"{out_dir}/{root_catalog_name}.json", "w", encoding="utf-8") as f:
#         json.dump(catalog_data, f, ensure_ascii=False, indent=4)

def create_stac_catalog_root(out_name):
    stem = Path(out_name).stem
    root_catalog_name = '_'.join(stem.split('_')[0:3])
    coll_checked = '_'.join(stem.split('_')[0:2])
    if 'doc_review' in out_name:
        collection_name = 'qa_documentation'
    elif 'radiometric_unc' in out_name:
        collection_name = 'qa_radiometric'
    # if 'doc_review' in out_name:
    catalog_data = {
        "stac_version": "1.0.0",
        "id": f"{root_catalog_name}",  # catalog_name #f"{stem}_catalog_{daterange.replace(',', '_')}
        "type": "Catalog",
        "description": f"Root catalog for {coll_checked} QA checks",
        "links": [
            {"type": "application/json", "rel": "self", "href": "catalog.json"},
            # {"type": "application/json", "rel": "child", "href": f"{root_catalog_name}.json"},
            {"type": "application/json", "rel": "child", "href": f"{collection_name}.json"},
        ],
    }
    with open(f"{out_dir}/catalog.json", "w", encoding="utf-8") as f:
        json.dump(catalog_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # sys_argv = ['/opt/project/qa_workflow_test/qa-workflow-test/__main__.py', 's3_endpoint']  # for testing locally with cwltool
    run_check(sys.argv)

    # # TEST CHECK WORKS LOCALLY
    # run_check([None, "AccessPointName-AccountId.s3-accesspoint.region.amazonaws.com", "radiometric_unc",
    #          "2022-01-01,2022-12-31", "s2"])
    # run_check([None, "AccessPointName-AccountId.s3-accesspoint.region.amazonaws.com", "doc_review",
    #          '2025-03-25', "planet"])
