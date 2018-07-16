import sys
import numpy as np
import pandas as pd
from scipy import stats


OUTPUT_TEMPLATE = (
    '"Did more/less users use the search feature?" p-value: {more_users_p:.3g}\n'
    '"Did users search more/less?" p-value: {more_searches_p:.3g}\n'
    '"Did more/less instructors use the search feature?" p-value: {more_instr_p:.3g}\n'
    '"Did instructors search more/less?" p-value: {more_instr_searches_p:.3g}'
)


def main():
    searchdata_file = sys.argv[1]
    searches = pd.read_json(searchdata_file, orient='records', lines=True)
    #print(searches)

    #get users_p
    evenuid_searched = searches[(searches['uid'] % 2 == 0) & (searches['search_count'] > 0)]['uid'].count()
    odduid_searched = searches[(searches['uid'] % 2 != 0) & (searches['search_count'] > 0)]['uid'].count()
    evenuid_neversearched = searches[(searches['uid'] % 2 == 0) & (searches['search_count'] == 0)]['uid'].count()
    odduid_neversearched = searches[(searches['uid'] % 2 != 0) & (searches['search_count'] == 0)]['uid'].count()
    uid_table = ([evenuid_searched,evenuid_neversearched],[odduid_searched,odduid_neversearched])
    #print (uid_table)
    chi2,users_p,dof,expected = stats.chi2_contingency(uid_table)

    #get searches_p
    oddsearched = searches[searches['uid'] % 2 != 0]['search_count']
    evensearched = searches[searches['uid'] % 2 == 0]['search_count']
    searches_p = stats.mannwhitneyu(oddsearched,evensearched).pvalue

    #get instr_p
    instr = searches[searches['is_instructor'] == True]
    evenuid_searched2 = instr[(instr['uid'] % 2 == 0) & (instr['search_count'] > 0)]['uid'].count()
    odduid_searched2 = instr[(instr['uid'] % 2 != 0) & (instr['search_count'] > 0)]['uid'].count()
    evenuid_neversearched2 = instr[(instr['uid'] % 2 == 0) & (instr['search_count'] == 0)]['uid'].count()
    odduid_neversearched2 = instr[(instr['uid'] % 2 != 0) & (instr['search_count'] == 0)]['uid'].count()
    uid_table2 = ([evenuid_searched2,evenuid_neversearched2],[odduid_searched2,odduid_neversearched2])
    #print (uid_table)
    chi2,instr_p,dof,expected = stats.chi2_contingency(uid_table2)

    #get instr_search_p
    oddsearched2 = instr[instr['uid'] % 2 != 0]['search_count']
    evensearched2 = instr[instr['uid'] % 2 == 0]['search_count']
    instr_search_p = stats.mannwhitneyu(oddsearched2,evensearched2).pvalue
    # Output
    print(OUTPUT_TEMPLATE.format(
        more_users_p = users_p,
        more_searches_p = searches_p,
        more_instr_p = instr_p,
        more_instr_searches_p = instr_search_p,
    ))


if __name__ == '__main__':
    main()
