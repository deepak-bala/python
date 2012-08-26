# Released under MIT license - http://opensource.org/licenses/mit-license.php

import pandas as pd
import math

VISA_CLASS = 'VISA_CLASS'
EMPLOYER_NAME = 'LCA_CASE_EMPLOYER_NAME'
EMPLOYER_CITY = 'LCA_CASE_EMPLOYER_CITY'
EMPLOYER_STATE = 'LCA_CASE_EMPLOYER_STATE'
JOB_TITLE = 'LCA_CASE_JOB_TITLE'
STATUS = 'STATUS'
STATUS_CERTIFIED = 'CERTIFIED'
RATE_FROM = 'LCA_CASE_WAGE_RATE_FROM'
WAGE_RATE_UNIT = 'LCA_CASE_WAGE_RATE_UNIT'
WAGE_RATE_UNIT_YEAR = 'Year'
WAGE_RATE_UNIT_HOUR = 'Hour'
WAGE_RATE_UNIT_MONTH = 'Month'
WAGE_RATE_UNIT_WEEK = 'Week'
WAGE_RATE_UNIT_BI_WEEK = 'Bi-Weekly'

COUNT_CERTIFIED = 0

def main():
    top = 10
    main_frame_chunks = pd.read_csv('/path/to/LCAFY2012_Q2.csv')
    print('Finished reading data')
    main_frame_len = len(main_frame_chunks)
    print('Processing ' + str(main_frame_len) + ' rows' )
    main_frame_chunks = main_frame_chunks.apply(normalize_sal, axis=1)
    print('Finished normalizing data')

    pretty_print('Most sought after VISAs')
    print(main_frame_chunks[VISA_CLASS].value_counts())

    pretty_print('Top ten job titles')
    print(main_frame_chunks[JOB_TITLE].value_counts()[:10])

    pretty_print('Employers with most number of VISAS in any status')
    name_group = main_frame_chunks.groupby([main_frame_chunks [EMPLOYER_NAME], main_frame_chunks[STATUS]])
    name_copy_group = name_group[STATUS].count().copy()
    name_copy_group.sort()
    print(name_copy_group[-top:])

    main_frame_chunks = main_frame_chunks.apply(drop_non_certified, axis=1)
    pretty_print(str(COUNT_CERTIFIED) + ' VISAs are certified and ' + str(main_frame_len - COUNT_CERTIFIED) + ' are not')

    pretty_print('Employers with the highest salary budget')
    grouped = main_frame_chunks.groupby( [EMPLOYER_NAME]  )
    grouped_sum = grouped.sum()
    copy_group = grouped_sum[RATE_FROM].copy()
    copy_group.sort()
    print(copy_group[-top:])

    pretty_print('The city offering the highest dough (summed over all positions)')
    city_st_group = main_frame_chunks.groupby([main_frame_chunks [EMPLOYER_CITY], main_frame_chunks[EMPLOYER_STATE] ])
    city_st_group_cp = city_st_group[RATE_FROM].sum().copy()
    city_st_group_cp.sort()
    print(city_st_group_cp[-top:])

    pretty_print('Jobs with the most dough (summed across offers from all employers)')
    job_title_group = main_frame_chunks.groupby([main_frame_chunks [JOB_TITLE]])
    job_title_group_cp = job_title_group[RATE_FROM].sum().copy()
    job_title_group_cp.sort()
    print(job_title_group_cp[-top:])

    print('Done')


def normalize_sal(x):
#    Normalize salary to a year
    if x.ix[RATE_FROM] is None or "" or math.isnan(x.ix[RATE_FROM]) or x.ix[RATE_FROM] > 1000000:
        x.ix[RATE_FROM] = 0
    if x.ix[WAGE_RATE_UNIT] == WAGE_RATE_UNIT_HOUR:
        x.ix[RATE_FROM] *=  (8 * 240)
    elif x.ix[WAGE_RATE_UNIT] == WAGE_RATE_UNIT_MONTH:
        x.ix[RATE_FROM] *= 12
    elif x.ix[WAGE_RATE_UNIT] == WAGE_RATE_UNIT_BI_WEEK:
        x.ix[RATE_FROM] *= 52 / 2
    elif x.ix[WAGE_RATE_UNIT] == WAGE_RATE_UNIT_WEEK:
        x.ix[RATE_FROM] *= 52
#    Clean employer name
    if isinstance(x[EMPLOYER_NAME],str):
        x[EMPLOYER_NAME] = x[EMPLOYER_NAME].replace('.','').strip()
    return x

def drop_non_certified(y):
    global COUNT_CERTIFIED
    if y.ix[STATUS] != STATUS_CERTIFIED:
        y.ix[RATE_FROM] = 0
    else:
         COUNT_CERTIFIED += 1
    return y


def pretty_print(name):
    print("********************************************************")
    print(name)
    print("********************************************************")

main()
