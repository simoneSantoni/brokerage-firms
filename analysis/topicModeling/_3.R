# tested against R 3.6.3
#
# Docstring
#-------------------------------------------------------------------------------
#      3.r    |    sequence analysis of dominant topics        
#-------------------------------------------------------------------------------
#
# Author:
#
# Edits: 
#       - created on
#       - last change
#
# Notes:
#


# %% load libraries
library(TraMineR)

# %% set wd
setwd(dir = '~/githubRepos/digital-leadership-center/analysis/topicModeling')

# %% read data
dt <- read.csv(file = '.output/ws_seq_analysis.csv')

# %% create a sequence object

# fix color palette
# ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple',
         'tab:gray', 'tab:pink', 'tab:brown']


colors <- c('#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
            '#7f7f7f', '#e377c2', '#8c564b')

dt.seq <- seqdef(dt, cpal = colors)

# %% visualize sequences


# create chart
outf = '.output/ws_seq_analysis.pdf'
pdf(outf)
par(mfrow = c(2, 2))
#seqiplot(dt.seq, with.legend = FALSE, border = NA)
seqIplot(dt.seq, with.legend = FALSE)
seqfplot(dt.seq, sortv = "from.start", with.legend = FALSE)
seqlegend(dt.seq)
dev.off()

