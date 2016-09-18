library(pvclust)
library(parallel)
#library(snow)
#library(Rmpi)
### example using Boston data in package MASS
input_file = "E:\\swang141\\project\\DreamDiseaseModule\\Sheng\\Data\\Embedding_vector\\DCA\\DCA_50dim.txt"
mydata =read.table(file = input_file)
## multiscale bootstrap resampling (non-parallel)

boston.pv <- pvclust(mydata, nboot=100)


pv_thres_l = c(0.9,0.95)

for (ii in 1:length(pv_thres_l))
{
  pv_thres <- pv_thres_l[ii]
## print clusters with high p-values
boston.pp <- pvpick(boston.pv,alpha=pv_thres,type="geq")


nclust <- length(boston.pp$clusters)
fileConn<-file(paste(c("output.txt",pv_thres),collapse=''),"w")
for (i in 1:(nclust))
{
  cat(file=fileConn, i,"1.0", paste(unlist(boston.pp$clusters[i]), collapse = '\t'), "\n")
print(paste(unlist(boston.pp$clusters[i]), collapse = '\t'))
  #writeLines(paste(unlist(boston.pp$clusters[i]), collapse = '\t'),fileConn,append=TRUE)
  #writeLines('\n', fileConn)
}
close(fileConn)
}


