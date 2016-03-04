#!/usr/bin/env python
##
##  Copyright 2015 SRI International
##  License: https://ncanda.sri.com/software-license.txt
##
##  $Revision: 2110 $
##  $LastChangedBy: nicholsn $
##  $LastChangedDate: 2015-08-07 09:10:29 -0700 (Fri, 07 Aug 2015) $
##
"""
Missing MRI Report
======================
Generate a report indicating which MRI Reports have not been entered.
"""
import os
import sys
import csv

import redcap
import pandas as pd

fields = ['study_id', 'redcap_event_name','exclude', 'visit_ignore',
          'visit_date','mri_missing', 'mri_xnat_sid','mri_series_t1',
          'mri_series_t2'];

forms=['mr_session_report', 'visit_date',
       'demographics'],

def get_project_entry(args=None):
	"""
	Pulls the data from REDCap
	"""
	# Get API key.
	summary_key_file = open(os.path.join(os.path.expanduser("~"),
	                                     '.server_config',
	                                     'redcap-dataentry-token'), 'r')
	summary_api_key = summary_key_file.read().strip()

	# Connect to API.
	project_entry = redcap.Project('https://ncanda.sri.com/redcap/api/',
	                               summary_api_key, verify_ssl=False)
	return project_entry

def data_entry_fields(fields,project,arm):
	"""
	Gets the dataframe containing a specific arm from REDCap
	"""
	# Get a dataframe of fields
	data_entry_raw = project.export_records(fields=fields, forms = forms, format='df', events=[arm])
	return data_entry_raw

def main(args=[visit, csv_file]):
    project_entry = get_project_entry()
    project_df = data_entry_fields(fields,project_entry,visit)

    ## Generate Subject List from csv
    with open(csv_file, 'rb') as f:
        reader = csv.reader(f)
        subject_list = map(tuple, reader)

    filter_df = project_df.filter(item = subject_list)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser('-v','--visit',choices=['baseline_visit_arm_1','1y_visit_arm_1'],default='1y_visit_arm_1')
    argv = parser.parse_args()
    sys.exit(main(args=argv))
