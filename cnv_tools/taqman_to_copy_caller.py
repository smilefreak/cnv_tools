#!/usr/bin/env python
#
#
#
#

taqman_header="""
SDS 2.4\tAQ Results\t\t1
Filename\t\tGene3 AMY1 31 March 2015        
PlateID         
Assay Type\tAbsolute Quantification     
Run DateTime\t31/03/15 8:32       
Operator            
ThermalCycleParams          
                
Sample Information          
                            
"""

taqman_top_row="""
Well\tPlate Position\tSample Name\tDetector Name\tReporter\tTask\tCt\tTm Value\tTm Type\tQuantity\tQty Mean\tQty StdDev\tCt Median\tCt Mean\tCt StdDev\tCt Type\tTemplate Name\tBaseline Type\tBaseline Start\tBaseline Stop\tThreshold Type\tThreshold\tFOS\tHMD\tLME\tEW\tBPR\tNAW\tHNS\tHRN\tEAF\tBAF\tTAF\tCAF
"""

mid_filler="""
R^2
Slope\tcycles/log decade
Y-Intercept
"""

sample_line="""sample\tmean_ct\tmedian_ct\tsd
"""

import argparse
import numpy as np
import sys

def print_data_line(idx,sample, num, m1, sd, med, fam=True):
    out_line = []
    out_line.append(str(idx + 1))
    out_line.append('TEST')
    out_line.append(sample)
    if fam:
        out_line.append('TAR')
        out_line.append('FAM')
    else:
        out_line.append('REF')
        out_line.append('VIC')
    out_line.append('Unknown')
    out_line.append(str(num))
    out_line.extend([""]*5)
    out_line.append(str(m1))
    out_line.append(str(med))
    out_line.append(str(sd))
    out_line.append("Manual Ct")
    out_line.append("")
    out_line.append("Automatic")
    out_line.append("")
    out_line.append("")
    out_line.append("Manual")
    out_line.append("0.2")
    print '\t'.join(out_line)

def process_file(p_file, samples,fam=True): 
    file_array = []
    with open(p_file) as f:
        for i, line in enumerate(f):
            if i > 1: 
                file_array.append(line.strip())
    all_cts = []
    other_data = []
    med_mean = []
    for k in range(8):
        for i in range(16):
            nums = []
            lines = []
            for j in range(3):
                idx = k * 48 + (i)  +  (j *16)
                l_s = file_array[idx].split()
                lines.append(l_s)
                cts = float(l_s[5])
                nums.append(cts)
                all_cts.append(cts)
                other_data.append(l_s)
            sample = samples[ k * 16 + i ]
            nums = np.array(nums)
            m1 = np.mean(nums)
            sd = np.std(nums)
            med = np.median(nums)
            med_mean.extend([[med, m1, sd],[med, m1, sd],[med, m1, sd]])
            for x in range(3):
                sys.stderr.write(str(k * 48 + i * 3 + x) + '\n')
                print_data_line(k * 48 + i* 3 + x, sample,  nums[x] ,m1,sd,med,fam)


def print_r_data(reference_file, target_file, samples):
    """
        Function processes a qPCR run and outputs R data files
    """
    print sample_line, 
    file_array1 = []
    file_array2 = []
    with open(reference_file) as f:
        for i, line in enumerate(f):
            if i > 1: 
                file_array1.append(line.strip())
    with open(target_file) as f:
        for i, line in enumerate(f):
            if i > 1: 
                file_array2.append(line.strip())
    all_cts = []
    other_data = []
    med_mean = []
    for k in range(8):
        for i in range(16):
            nums = []
            lines = []
            for j in range(3):
                idx = k * 48 + (i)  +  (j *16)
                l_s1 = file_array1[idx].split()
                l_s2 = file_array2[idx].split()
                lines.append(l_s1)
                lines.append(l_s2)
                cp = float(l_s2[5]) - float(l_s1[5])
                nums.append(cp)
                all_cts.append(cp)
                other_data.append(l_s1)
            sample = samples[ k * 16 + i ]
            nums = np.array(nums)
            m1 = np.mean(nums)
            sd = np.std(nums)
            med = np.median(nums)
            med_mean.extend([[med, m1, sd],[med, m1, sd],[med, m1, sd]])
            print '\t'.join([sample, str(m1),str(med), str(sd)])

def get_sample(sample_file):
    samples = [] 
    with open(sample_file) as f:
        for line in f:
            samples.append(line.strip().split()[0])
    return samples

def print_data(target_file, reference_file, sample_file, create_r_data):
    """
        Print data for conversion to copy caller format.
    """
    samples = get_sample(sample_file)
    file_array = []
    if not create_r_data:
        print taqman_header
        print taqman_top_row,
        process_file(target_file, samples,fam=True, create_r_data=r_data)
        print mid_filler
        print taqman_top_row,
        process_file(reference_file, samples, fam=False, create_r_data=r_data)
    else:
        print_r_data(reference_file, target_file, samples)

def main():
        parser = argparse.ArgumentParser(description="Copy caller format")
        parser.add_argument("-t","--target",dest="target", help="Target input file", required=True)
        parser.add_argument('-r','--reference',dest="reference", help="Reference input file", required=True)
        parser.add_argument('-s','--sample-list', dest='sample_list', help='Sample list', required=True)
        parser.add_argument('-R','--r-data', dest='create_r_data', help='Create R data instead of data for copy caller', action='store_true')
        args = parser.parse_args()
        print_data(args.target,args.reference, args.sample_list, args.create_r_data)

if __name__=="__main__":
    main()
