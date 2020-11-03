#

rule generate_feature_bounds:
    output:
        './output/chromosome_intervals.tsv'
    run:
        c = 'python create_genome_bounds.py'
        shell(c)

rule create_intergenic_intervals:
    input:
        './output/chromosome_intervals.tsv'
    output:
        './output/intergenic_intervals.tsv'
    run:
        c = 'python create_intergenic_intervals.py {input}'
        shell(c)

rule augment_intergenic_intervals:
    input:
        './output/intergenic_intervals.tsv'
    output:
        './output/intergenic_intervals_with_gene_buffers.tsv'
    run:
        c = 'python augment_intergentic_intervals_around_genes.py {input} {output} 1000'
        shell(c)

rule create_quantifiable_intervals:
    input:
        './output/intergenic_intervals_with_gene_buffers.tsv'
    output:
        './output/intergenic_intervals_for_quantification.200_bp.tsv'
    run:
        c = 'python create_quantifiable_intervals.py {input} {output} 200'
        shell(c)

rule assign_ATAC_seq_reads_to_intervals:
    input:
        intervals='./output/intergenic_intervals_for_quantification.200_bp.tsv',
        bam='./ENCSR885DVH/ENCFF251PDI.bam'
    output:
        './output/ENCSR885DVH_ENCFF251PDI.interval_counts.200_bp.tsv'
    run:
        c = 'python assign_reads_to_intervals.py {input.intervals} {input.bam} {output}'
        shell(c)

rule assign_RNA_seq_reads_to_intervals:
    input:
        intervals='./output/intergenic_intervals_for_quantification.200_bp.tsv',
        bam='./ENCSR885DVH/ENCFF625ZBS.bam'
    output:
        './output/ENCSR885DVH_ENCFF625ZBS.interval_counts.200_bp.tsv'
    run:
        c = 'python assign_reads_to_intervals.py {input.intervals} {input.bam} {output}'
        shell(c)

## Interval size of 400
rule create_quantifiable_intervals_400bp:
    input:
        './output/intergenic_intervals_with_gene_buffers.tsv'
    output:
        './output/intergenic_intervals_for_quantification.400_bp.tsv'
    run:
        c = 'python create_quantifiable_intervals.py {input} {output} 400'
        shell(c)

