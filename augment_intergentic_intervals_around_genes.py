import pandas as pd
import sys

def main():

    intervals_f = sys.argv[1]
    out_f = sys.argv[2]
    gene_clearance = int(sys.argv[3])
    
    intrs_df = pd.read_csv(intervals_f, sep='\t', index_col=False)
    da = []

    chrm = None
    for r_i, row in intrs_df.iterrows():
        chrm = row['chromosome']
        begin = row['interval_begin']
        end = row['interval_end']
        new_begin = begin + gene_clearance
        new_end = end - gene_clearance
        if new_begin < new_end:
            da.append((
                chrm,
                new_begin,
                new_end,
                new_end - new_begin
            ))
    df = pd.DataFrame(
        data=da,
        columns=['chromosome', 'interval_begin', 'interval_end', 'length']
    )
    df.to_csv(out_f, sep='\t', index=None)
        

if __name__ == '__main__':
    main()
