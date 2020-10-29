import pandas as pd
import sys
import numpy as np
import pysam

def main():
    intervals_f = sys.argv[1]
    bam_f = sys.argv[2]
    out_f = sys.argv[3]
    
    intrs_df = pd.read_csv(intervals_f, sep='\t', index_col=False)

    bam = pysam.AlignmentFile(bam_f, 'rb')


    da = []
    for r_i, row in intrs_df.iterrows():
        if r_i % 10000 == 0:
            print("Computing reads in interval {}/{}".format(r_i, len(intrs_df)))
        int_id = row['interval_id']
        chrm = row['chromosome']
        begin = row['interval_begin']
        end = row['interval_end']
        
        reads = list(bam.fetch(chrm, begin, end))
        da.append((int_id, chrm, begin, end, len(reads)))

    df = pd.DataFrame(
        data=da,
        columns=['interval_id', 'chromosome', 'interval_begin', 'interval_end', 'n_reads']
    )
    df = df.set_index('interval_id')
    print("Writing to {}".format(out_f))
    df.to_csv(out_f, sep='\t')
        

if __name__ == '__main__':
    main()
