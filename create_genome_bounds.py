import pysam
import numpy as np
from BCBio import GFF
import pandas as pd

CHRM_TO_LEN = {
    'chr1': 248956422
}
INTERVAL_SIZE = 1000
GFF_F = 'gencode.v24.annotation.gff3'

class IntervalBoundary:
    def __init__(self, chrm, coord, btype, ftype, name):
        self.chrm = chrm
        self.coord = coord
        self.btype = btype
        self.ftype = ftype
        self.name = name
        
    def __repr__(self):
        return str(self.__dict__)


def main():
    atac_bam = './ENCSR885DVH/ENCFF251PDI.bam'
    rna_bam = './ENCSR885DVH/ENCFF625ZBS.bam'

    atac_samfile = pysam.AlignmentFile(atac_bam, 'rb')
    rna_samfile = pysam.AlignmentFile(rna_bam, 'rb')

    interval_bounds = []

    with open(GFF_F, 'r') as f:
        gff = GFF.parse(f)
        for i, rec in enumerate(gff):
            print("Processing record {}".format(rec.id))
            curr_intervals = []
            for fi, feat in enumerate(rec.features):
                curr_intervals.append(
                    IntervalBoundary(
                        rec.id,
                        feat.location.start.position,
                        'start',
                        feat.type,
                        feat.id
                    )
                )
                curr_intervals.append(
                    IntervalBoundary(
                        rec.id,
                        feat.location.end.position,
                        'end',
                        feat.type,
                        feat.id
                    )
                )
            curr_intervals = sorted(
                curr_intervals,
                key=lambda x: x.coord
            )
            print(len(curr_intervals))
            interval_bounds += curr_intervals
    da = [
        [b.chrm, b.coord, b.btype, b.ftype, b.name]
        for b in interval_bounds
    ]
    df = pd.DataFrame(
        data=da,
        columns=['chromosome', 'coordinate', 'boundary_type', 'feature_type', 'feature_name']
    )

    df.to_csv(
        'chromosome_intervals.tsv',
        sep='\t',
        index=None
    )
        


if __name__ == '__main__':
    main()
