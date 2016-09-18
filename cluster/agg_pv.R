library(pvclust)
### example using Boston data in package MASS
data(Boston, package = "MASS")
## multiscale bootstrap resampling (non-parallel)
boston.pv <- pvclust(Boston, nboot=100, parallel=FALSE)


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


