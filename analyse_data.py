import sys
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

def main():
    data = pd.read_csv('data.csv')
    #print (data)
    # anova test
    anova = stats.f_oneway(data['qs1'], data['qs2'], data['qs3'], data['qs4'], data['qs5'], data['merge1'], data['partition_sort'])
    print("\033[1;48m-------Anova Test------\033[1;m")
    print(anova)
    print("Because p < 0.05 in anova, we can then do post hoc analysis" + "\n\n")


    # post hoc Tukey test
    x_data = pd.DataFrame({'qs1':data['qs1'], 'qs2':data['qs2'], 'qs3':data['qs3'], 'qs4':data['qs4'],'qs5':data['qs5'], 'merge1':data['merge1'], 'partition_sort':data['partition_sort'] })
    x_melt = pd.melt(x_data)
    posthoc = pairwise_tukeyhsd(
        x_melt['value'], x_melt['variable'],
        alpha=0.05)
    print("\033[1;48m-------Post Hoc Tukey Test------\033[1;m")
    print (posthoc)
    print("\n\n")

    # get mean value to all different
    print("\033[1;48m-------Mean Value------\033[1;m")
    print('qs1.mean: ',data['qs1'].mean())
    print('qs2.mean: ',data['qs2'].mean())
    print('qs3.mean: ',data['qs3'].mean())
    print('qs4.mean: ',data['qs4'].mean())
    print('qs5.mean: ',data['qs5'].mean())
    print('merge1.mean: ',data['merge1'].mean())
    print('partition_sort.mean: ',data['partition_sort'].mean())


if __name__ == '__main__':
    main()
