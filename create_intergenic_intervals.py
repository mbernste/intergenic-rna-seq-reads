import pandas as pd

def main():
    bounds_df = pd.read_csv('./output/chromosome_intervals.tsv', sep='\t', index_col=False)
    da = []
    for chrm in sorted(set(bounds_df['chromosome'])):
        print('Creating intervals for chromosome {}'.format(chrm))
        chrm_df = bounds_df.loc[bounds_df['chromosome'] == chrm]
        chrm_df = chrm_df.sort_values(by='coordinate')
        open_genes = set()
        curr_begin = 0
        intervals = []
        for r_i, row in chrm_df.iterrows():
            btype = row['boundary_type']
            feat_name = row['feature_name']
            coord = row['coordinate']
            if len(open_genes) == 0:
                # We've reached the end of an intergenic interval.
                # The next boundary type must begin a new gene, so
                # we should cap off the current intergenic interval.
                assert btype == 'start'
                intervals.append((curr_begin, coord))
                open_genes.add(feat_name)
            else:
                if btype == 'start':
                    # We are in the midst of a genic
                    # interval in which a new gene begins
                    open_genes.add(feat_name) 
                elif btype == 'end':
                    open_genes.remove(feat_name)
                    # We are no longer in any genes, so we 
                    # should begin a new intergenic interval
                    if len(open_genes) == 0:
                        curr_begin = coord
        da += [
            [chrm, intr[0], intr[1], intr[1]-intr[0]]
            for intr in intervals
        ]
    df = pd.DataFrame(
        data=da,
        columns=['chromosome', 'interval_begin', 'interval_end', 'length']
    )
    df.to_csv('intergenic_intervals.tsv', sep='\t', index=None)

if __name__ == '__main__':
    main()
