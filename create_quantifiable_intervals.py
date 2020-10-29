import pandas as pd
import sys
import numpy as np

def main():
    intervals_f = sys.argv[1]
    out_f = sys.argv[2]
    interval_size = int(sys.argv[3])
    
    intrs_df = pd.read_csv(intervals_f, sep='\t', index_col=False)
    da = []

    #chrm_counter = 0
    curr_chrm = intrs_df.iloc[0]['chromosome']
    for r_i, row in intrs_df.iterrows():
        chrm = row['chromosome']
        begin = row['interval_begin']
        end = row['interval_end']

        # Reset the counter for counting the
        # subintervals along each chromosome
        #if curr_chrm != chrm:
        #    curr_chrm = chrm
        #    chrm_counter = 0

        # Compute the subintervals
        sub_ints = list(np.arange(begin, end, interval_size))
        if sub_ints[-1] < end:
            sub_ints.append(end)
        for i in range(len(sub_ints[:-1])):
            da.append((
                '{}.{}_{}'.format(chrm, sub_ints[i], sub_ints[i+1]),
                chrm,
                sub_ints[i],
                sub_ints[i+1]  
            ))
            #chrm_counter += 1

    df = pd.DataFrame(
        data=da,
        columns=['interval_id', 'chromosome', 'interval_begin', 'interval_end']
    )
    df = df.set_index('interval_id')
    df.to_csv(out_f, sep='\t')
        

if __name__ == '__main__':
    main()
