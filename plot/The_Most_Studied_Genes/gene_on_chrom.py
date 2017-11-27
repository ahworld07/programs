#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
usage:
    plot genes on chromosome
    python3 g.pene_on_chrom.py -i gene_info_total_human.tsv

Created on Sun Nov 11 23:23 2017
author: Zan Yuan
email: seqyuan@gmail.com
github: github.com/seqyuan
blog: www.seqyuan.com
WeChat Official Account: seqyuan
"""

import os
import sys
import pandas as pd
import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import warnings
warnings.filterwarnings("ignore")
import argparse
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

class chrom_class:
    df_chrominfo = None
    df_cytoband = None
    df_gene_citation_counts = None
    pad = 0

    def Init_read_file(self,chromInfo,cytoBand,all_gene_counts_file):
        df_gene_citation_counts = pd.read_table(all_gene_counts_file,header=None,index_col=None,names=['9606','un','id','chrom','start','end','name','describe','funcclass','citations'],encoding='utf-8')
        self.df_gene_citation_counts = df_gene_citation_counts.sort_values(by=['citations'],ascending=False)
        self.df_gene_citation_counts['Ranking'] = list(range(1,df_gene_citation_counts.shape[0] + 1))
        self.df_gene_citation_counts['citations'] = df_gene_citation_counts['citations']/(df_gene_citation_counts['citations'].max() * 1.2)

        df_cytoband = pd.read_table(cytoBand,header=None,index_col=None,names=['chrom','start','end','p','c'],encoding='utf-8')
        self.df_chrominfo = pd.read_table(chromInfo,header=None,index_col=None,names=['chrom','length','s'],encoding='utf-8')

        self.df_cytoband = df_cytoband[df_cytoband['c'] == 'acen']
        self.pad = self.df_chrominfo['length'].max().max() * 0.012

    def plot_Rounded_Rectangle(self,ax):
        for i, row in self.df_chrominfo.iterrows():
            chr_cen = self.df_cytoband[self.df_cytoband['chrom'] ==row['chrom']][['start','end']]
            chr_cen_start = chr_cen.min().min()
            chr_cen_end = chr_cen.max().max()
            boxstyle = "round,pad={0}".format(self.pad)

            left_Rectangle = FancyBboxPatch((0+self.pad, (i*9+1)*self.pad), chr_cen_start - self.pad * 2, self.pad * 6, boxstyle=boxstyle, facecolor='#313131', edgecolor='#313131')
            right_Rectangle = FancyBboxPatch((chr_cen_end + self.pad, (i*9+1)*self.pad), row['length'] - chr_cen_end - self.pad * 2, self.pad * 6, boxstyle=boxstyle, facecolor='#313131', edgecolor='#313131')
            cent_Rectangle = FancyBboxPatch((chr_cen_start, (i*9+3)*self.pad), chr_cen_end - chr_cen_start, self.pad * 2, boxstyle="square,pad=0", facecolor='#313131', edgecolor='#313131')            
            ax.add_patch(left_Rectangle)
            ax.add_patch(right_Rectangle)
            ax.add_patch(cent_Rectangle)
            ax.text(self.pad*0.2, (i*9+2)*self.pad, row['chrom'].lstrip('chr'), ha='left', va= 'center',fontsize=7,color='y',fontweight='bold')

            chrom_df = self.df_gene_citation_counts[self.df_gene_citation_counts['chrom'] == row['chrom']]
            print (chrom_df)
            width = list(chrom_df['end'] - chrom_df['start'])
            ax.bar(bottom=[(i*10)*self.pad] * len(width), width=width, height=chrom_df['citations'],left=chrom_df['start'],color='y',edgecolor='y',align='center',alpha=1)

        ax.set_yticks([])
        ax.set_yticklabels([])
        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.tick_params(bottom ='off',top='off',left='off',right='off')
        ax.set_xlim([0,self.df_chrominfo['length'].describe().max()])
        ax.set_ylim([self.df_chrominfo.shape[0] * self.pad *10, 0])



def main(args):
    all_gene_counts_file, chromInfo, cytoBand = args
    fig = plt.figure(figsize=(8,30),facecolor='k')
    #fig.patch.set_facecolor('black')

    [ax_x, ax_y, ax_w, ax_h] = [0.05,0.03,0.7,0.9]
    ax_chrom = fig.add_axes([ax_x, ax_y, ax_w, ax_h], frame_on=False, axisbg = 'k')
    
    chrom = chrom_class()
    chrom.Init_read_file(chromInfo, cytoBand, all_gene_counts_file)

    chrom.plot_Rounded_Rectangle(ax_chrom)


    plt.show()
    fig.savefig('jg.pdf')

if __name__ == '__main__':
    args = ['all_gene_counts.tsv','chromInfo.txt','cytoBand.txt']
    main(args)