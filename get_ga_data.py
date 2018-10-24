import csv
import logging
import os
from datetime import date
from datetime import datetime
from typing import List

import logzero
from apiclient.discovery import build
from logzero import logger
from oauth2client.service_account import ServiceAccountCredentials

log_file = 'log/get_ga_data.log'

log_format = '%(color)s' \
             '[%(levelname)-5.5s ' \
             '%(asctime)-15s ' \
             '%(module)s:%(lineno)d]' \
             '%(end_color)s ' \
             '%(message)s'

formatter = logzero.LogFormatter(fmt=log_format, datefmt='%Y-%m-%d %H:%M:%S')
logzero.setup_default_logger(
    logfile=log_file,
    formatter=formatter,
    maxBytes=(1048576 * 5),
    backupCount=7,
    level=logging.INFO,
)

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'credentials/google_analytics.json'
PROJECT_VIEW_ID = '63448190'

FEED_DATA_FILE: str = 'data/output/access_history_ga.csv'

start_date: str = '2012-08-28'  # '7daysAgo'
max_results = '3000'


def initialize_analyticsreporting():
    """Initializes an Analytics Reporting API V4 service object.

  Returns:
    An authorized Analytics Reporting API V4 service object.
  """

    # Build the credentials object
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES,
    )
    # Build the service object.
    analytics = build('analyticsreporting', 'v4', credentials=credentials)
    return analytics


def get_report(analytics):
    """Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """
    # https://developers.google.com/analytics/devguides/reporting/core/v4/rest/
    # https://analyticsreporting.googleapis.com/$discovery/rest?version=v4
    # https://developers.google.com/analytics/devguides/reporting/core/v4/basics
    return analytics.reports().batchGet(
        prettyPrint=True,
        body={
            'reportRequests': [
                dict(
                    viewId=PROJECT_VIEW_ID,
                    dateRanges=[
                        {
                            'startDate': start_date,
                            'endDate': 'yesterday',
                        },
                    ],
                    metrics=[
                        {'expression': 'ga:users'},  # ,
                        # {'expression': 'ga:newUsers'},
                    ], dimensions=[
                        {'name': 'ga:date'},
                    ], orderBys=[
                        {'fieldName': 'ga:date', 'sortOrder': 'DESCENDING'},
                    ], pageSize=max_results,
                ),
            ],
        },
    ).execute()


def save_report_data(results):
    """Prints out the results. """
    if os.path.isfile(FEED_DATA_FILE):
        pass

    csv_file = open(FEED_DATA_FILE, 'wt', encoding='utf-8')
    writer = csv.writer(csv_file, lineterminator='\n')

    for report in results.get('reports', []):
        column_header = report.get('columnHeader', {})
        dimension_headers = column_header.get('dimensions', [])
        metric_headers = column_header.get(
            'metricHeader', {},
        ).get('metricHeaderEntries', [])
        rows = report.get('data', {}).get('rows', [])

        header_row = []
        header_row.extend(dimension_headers)
        header_row.extend([mh['name'] for mh in metric_headers])

        logger.debug(header_row)
        writer.writerow(header_row)

        for row in rows:
            dimensions_data = row.get('dimensions', [])
            access_date = ''.join(dimensions_data[0])
            _date: date = datetime.strptime(access_date, '%Y%m%d').date()
            metrics_data = [m['values'] for m in row.get('metrics', [])][0]

            data_row: List[str] = [str(_date)]
            data_row.extend(metrics_data)
            logger.debug(data_row)
            writer.writerow(data_row)

    # Close the file.
    csv_file.close()


# https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/installed-py
# https://ga-dev-tools.appspot.com/query-explorer/
def main():
    logger.info('Initiate Connection To Google Analytics')
    analytics = initialize_analyticsreporting()
    logger.info('Execute batch Query')
    response = get_report(analytics)
    logging.debug('Report response: {0}'.format(response))
    logger.info('Save Data To CSV')
    save_report_data(response)
    logger.info('Google Analytics Data Successfully Downloaded')


if __name__ == '__main__':
    main()
