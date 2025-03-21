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


def do_func(args):
    s3 = boto3.client("s3")  #- not needed?
    s3_endpoint = args[1]
    daterange = args[2]  # '2022-01-01,2022-12-31'
    data_collection = args[3]  # 'planet'

    # get from date range
    dates_list = get_dates_list(daterange)

    # set the environment variable for the S3 endpoint, in the future this will be set outside of the code.
    os.environ["AWS_S3_ENDPOINT"] = s3_endpoint

    # name stac item/catalog after qa check
    base_name = 'planet_psscene_qa_check_radiometric_unc'

    # get matchups for that time period
    sat = 'planet'
    site = 'RCN-GONA'
    url = f'http://db-api.eba-3ean8bmb.eu-west-2.elasticbeanstalk.com/matchups?sensor1={data_collection}&sensor2={site}&dates={daterange}'
    response = requests.get(url)
    mup_dict = json.loads(response.text)
    mup_ds = xr.Dataset.from_dict(mup_dict)

    if mup_ds:
        create_stac_items(base_name, mup_ds, daterange, dates_list)

        create_stac_catalog_root(base_name, daterange, dates_list)
    else:
        return

# get dates list from daterange input
def get_dates_list(daterange):
    return ['2022-01-01,2022-01-31',
            '2022-02-01,2022-02-28',
            '2022-03-01,2022-03-31',
            '2022-04-01,2022-04-30',
            '2022-05-01,2022-05-31',
            '2022-06-01,2022-06-30',
            '2022-07-01,2022-07-31',
            '2022-08-01,2022-08-31',
            '2022-09-01,2022-09-30',
            '2022-10-01,2022-10-31',
            '2022-11-01,2022-11-30',
            '2022-12-01,2022-12-31',
            ]

def qa_check_rad_val(mup_ds, date_range):

    dates = [date_range.split(',')[0], date_range.split(',')[1]]
    datetimes_range = [dt.datetime.strptime(dates[0], "%Y-%m-%d"), dt.datetime.strptime(dates[1], "%Y-%m-%d")]

    # remove nan values
    del_list_idx = []
    for j, arr in enumerate(mup_ds['planet_RCN-GONA_BiasVals'].values):
        if all(arr[i] == -9999 for i in range(13)):
            del_list_idx.append(j)

    mup_ds_bias_vals = np.delete(mup_ds['planet_RCN-GONA_BiasVals'].values, del_list_idx, axis=0)
    # mup_ds_bias_unc_vals = np.delete(mup_ds['planet_RCN-GONA_BiasUncVals'].values, del_list_idx, axis=0)
    mup_ds_rcn_meas_vals = np.delete(mup_ds['planet_RCN-GONA_MeasValsSensor2'].values, del_list_idx, axis=0)
    # mup_ds_rcn_meas_unc_vals = np.delete(mup_ds['planet_RCN-GONA_MeasValsUncSensor2'].values, del_list_idx, axis=0)

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
            # rcn_meas_unc_vals[j][k] = mup_ds_rcn_meas_unc_vals[k][j]

    # first keep only 8 bands for planet
    bias_vals = bias_vals[:8]
    # bias_unc_vals = bias_unc_vals[:8]
    rcn_meas_vals = rcn_meas_vals[:8]
    rcn_meas_unc_vals = np.ones(rcn_meas_vals.shape) * 0.9

    rcn_bias_vals_mean = np.ones(len(bias_vals)) * np.nan
    rcn_refl_vals_mean_unc = np.ones(len(bias_vals)) * np.nan  # todo: get rcn refl vals uncs through pipeline

    for k in range(len(bias_vals)):
        rcn_bias_vals_mean[k] = round(sum(bias_vals[k]) / len(bias_vals[k]), 2)
        rcn_refl_vals_mean_unc[k] = round(sum(rcn_meas_unc_vals[k]) / len(rcn_meas_unc_vals[k]), 2)  # todo: update once rcn refl uncs are through the pipeline


    psd_mean_unc = np.array([8.013, 6.798, 6.244, 5.636, 5.771, 6.277, 8.736, 9.229])
    psd_exp_val = "8.0% (coastal blue), 6.8% (blue), 6.2% (green_i), 5.6% (green_ii), 5.8% (yellow), 6.3% (red), 8.7% (red edge), 9.2% (NIR)",  # abs rad unc from doc: https://support.planet.com/hc/en-us/article_attachments/4403255608849 (log in here https://support.planet.com/hc/en-us/articles/360037649554-L1-Data-Quality-Reports-for-the-PlanetScope-Constellation)

    sat_mean_unc = psd_mean_unc
    stated_value = psd_exp_val
    rad_unc_report_title = "PLANET L1 DATA QUALITY REPORT, SUPERDOVE 8-BAND GENERAL AVAILABILITY: Status of Calibration and Data Quality for the SuperDove 8-Band GA, 15/06/21"
    rad_unc_report_ref = "https://support.planet.com/hc/en-us/articles/360037649554-L1-Data-Quality-Reports-for-the-PlanetScope-Constellation"
    sat_checked = "planet"
    doi ="https://staging.eodatahub.org.uk/api/catalogue/stac/catalogs/supported-datasets/catalogs/planet/collections/PSScene"


    comp_unc_vals = np.ones(len(sat_mean_unc)) * 2  # todo: update based on what comp unc should be

    total_unc = np.sqrt(
        sat_mean_unc ** 2 + rcn_refl_vals_mean_unc ** 2 + comp_unc_vals ** 2)  # total unc combines unc from sat product, unc from RCN product, unc from comparison

    # calc E
    e_val = rcn_bias_vals_mean / total_unc

    result_list = []
    for val in range(len(rcn_bias_vals_mean)):
        if abs(e_val[val]) <= 1:
            result_list.append('pass')
        elif abs(e_val[val]) <= 2:
            result_list.append('partial')
        else:  # if >2
            result_list.append('fail')

    if all([result_list[i] == 'pass' for i in range(len(result_list))]):
        result = 'pass'
    elif all([result_list[i] == 'fail' for i in range(len(result_list))]):
        result = 'fail'
    else:
        result = 'partial pass'

    qa_radiometric_check_result_output = {  # output dict of radiometric test result
        "data_collection": "PSScene",
        "data_id_field": doi,
        "uuid": "uuid",
        "check_name": "radiometric uncertainty",
        "results": {
            'data validation': {
                'radiometric uncertainty': {
                    "metric": "https://eodatahub.org.uk/api/ontologies/qa/metrics/data-validation/radiometric-uncertainty",
                    "value": result,
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


def create_stac_items(out_name, mup_ds, daterange, dates_list):
    for dates in dates_list:
        qa_check_results_dict = qa_check_rad_val(mup_ds, dates)

        stem = Path(out_name).stem  # later for "id": f"{stem}-{now}"
        # size = os.path.getsize(f"{out_name}")
        # mime = mimetypes.guess_type(f"{out_name}")[0]

        # dump qa result file
        with open(f"{out_dir}/output_{stem}_{dates.replace(',', '_')}.json", "w", encoding="utf-8") as f:
            json.dump(qa_check_results_dict, f, ensure_ascii=False, indent=4)

        data = dict(id = f"{stem}_{dates.replace(',', '_')}", #qa_check_results_dict["data_collection"].replace(" ", "_") + '_qa_check_test',
                    type = "Feature",
                    stac_version = "1.0.0",
                    geometry={  # GONA coords
                        "type": "Polygon",
                        "coordinates": [
                            [[15.10274,-23.60723694],
                             [15.13462891,-23.60723694],
                             [15.13462891,-23.59451068],
                             [15.10274,-23.59451068],
                             [15.10274,-23.60723694]]
                        ],
                    },
                    bbox=[15.10274,-23.60723694, 15.13462891,-23.59451068],  # GONA coords
                    properties={"datetime": qa_check_results_dict["check_datetime"],
                                "check_validity_start_datetime": qa_check_results_dict["check_datetime_validity_start"],
                                "check_validity_end_datetime": qa_check_results_dict["check_datetime_validity_end"]
                                },
                    links = [
                        {"type": "application/json", "rel": "self",  "href": f"{stem}_{dates.replace(',', '_')}.json"},
                        {"type": "application/json", "rel": "parent", "href": f"catalog.json"}, #f"{stem}_catalog_{daterange.replace(',', '_')}
                        {"type": "application/json", "rel": "root", "href": f"catalog.json"}, #f"{stem}_catalog_{daterange.replace(',', '_')}
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
                            # "title": f"output_{stem}_{dates.replace(',', '_')}",  # f"{stem}_catalog_{daterange.replace(',', '_')}
                            # "description": f"qa result output for {stem}_{dates.replace(',', '_')}",
                            "type": "application/json",
                            # "roles": ["data"],
                        },
                    },
                    )

        with open(f"{out_dir}/{stem}_{dates.replace(',', '_')}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


def create_stac_catalog_root(out_name, daterange, dates_list):
    stem = Path(out_name).stem
    data = {
        "stac_version": "1.0.0",
        "id": f"catalog", #f"{stem}_catalog_{daterange.replace(',', '_')}
        "type": "Catalog",
        "description": "Root catalog",
        "links": [
            {"type": "application/json", "rel": "item", "href": f"{stem}_{dates_list[0].replace(',', '_')}.json"},
            {"type": "application/json", "rel": "item", "href": f"{stem}_{dates_list[1].replace(',', '_')}.json"},
            {"type": "application/json", "rel": "item", "href": f"{stem}_{dates_list[1].replace(',', '_')}.json"},
            {"type": "application/json", "rel": "item", "href": f"{stem}_{dates_list[3].replace(',', '_')}.json"},
            {"type": "application/json", "rel": "item", "href": f"{stem}_{dates_list[4].replace(',', '_')}.json"},
            {"type": "application/json", "rel": "item", "href": f"{stem}_{dates_list[5].replace(',', '_')}.json"},
            {"type": "application/json", "rel": "item", "href": f"{stem}_{dates_list[6].replace(',', '_')}.json"},
            {"type": "application/json", "rel": "item", "href": f"{stem}_{dates_list[7].replace(',', '_')}.json"},
            {"type": "application/json", "rel": "item", "href": f"{stem}_{dates_list[8].replace(',', '_')}.json"},
            {"type": "application/json", "rel": "item", "href": f"{stem}_{dates_list[9].replace(',', '_')}.json"},
            {"type": "application/json", "rel": "item", "href": f"{stem}_{dates_list[10].replace(',', '_')}.json"},
            {"type": "application/json", "rel": "item", "href": f"{stem}_{dates_list[11].replace(',', '_')}.json"},
            {"type": "application/json", "rel": "self", "href": f"catalog.json"}, #f"{stem}_catalog_{daterange.replace(',', '_')}
        ],
    }
    with open(f"{out_dir}/catalog.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # sys_argv = ['/opt/project/qa_workflow_test/qa-workflow-test/__main__.py', 's3_endpoint']  # for testing locally
    do_func(sys.argv)

    # # TEST CHECK WORKS LOCALLY
    # do_func([None, "AccessPointName-AccountId.s3-accesspoint.region.amazonaws.com", "2022-01-01,2022-12-31", "planet"])

    # daterange = '2022-01-01,2022-12-31'
    # data_collection = 'planet'
    #
    # # get from date range
    # dates_list = ['2022-01-01,2022-01-31',
    #               '2022-02-01,2022-02-28',
    #               '2022-03-01,2022-03-31',
    #               '2022-04-01,2022-04-30',
    #               '2022-05-01,2022-05-31',
    #               '2022-06-01,2022-06-30',
    #               '2022-07-01,2022-07-31',
    #               '2022-08-01,2022-08-31',
    #               '2022-09-01,2022-09-30',
    #               '2022-10-01,2022-10-31',
    #               '2022-11-01,2022-11-30',
    #               '2022-12-01,2022-12-31',
    #               ]
    #
    # # name stac item/catalog after qa check
    # base_name = 'planet_psscene_qa_check_radiometric_unc'
    #
    # # get matchups for that time period
    # # sat = 'planet'
    # site = 'RCN-GONA'
    # url = f'http://db-api.eba-3ean8bmb.eu-west-2.elasticbeanstalk.com/matchups?sensor1={data_collection}&sensor2={site}&dates={daterange}'
    # response = requests.get(url)
    # mup_dict = json.loads(response.text)
    # mup_ds = xr.Dataset.from_dict(mup_dict)
    #
    # create_stac_items(base_name, mup_ds, daterange, dates_list)
    #
    # create_stac_catalog_root(base_name, daterange, dates_list)
