#!/usr/bin/env Rscript

file = 'path to the file'

title = 'Your title'
ylabel = 'Your y label'
xlabel = 'Your x label'

#Reading the data file
data = read.table(file, sep = ",")
#Creating a vector from the loaded data
data_vector = data[,2]

#Setting up the Poltting properties
attach(mtcars)
options(scipen=5)
family = 'sans'

len = length(data_vector)
xlim_max = max(data_vector)

#Creating a pdf to output the plot
pdf('plot.pdf', width=10, height=5)
par(mfrow=c(1,2))

#Plotting ECDF
plot(ecdf(data_vector), log="x", main="CDF", xlab=xlabel, ylab=ylabel, xlim=c(1, xlim_max))
grid(nx = NULL, ny = NULL, col = "lightgray", lty = "dotted", lwd = par("lwd"), equilogs = TRUE)

#CAlculating and plotting CCDF
plot(sort(data_vector) , ((1-ecdf(data_vector)(sort(data_vector)))*len ), log="xy", main="CCDF", xlab=xlabel, ylab=ylabel)
grid(nx = NULL, ny = NULL, col = "lightgray", lty = "dotted", lwd = par("lwd"), equilogs = TRUE)


#To show the common title 
title(title, outer=TRUE, line = -1.5)
dev.off()
