#setwd("D:/Geodawksp/keypoly2")
#setwd("D:/Geodawksp/exmaple")
library(spdep)
library(maptools)  #readShapePoly
library(geoR)   #boxcocfit
library(MASS)  # negative binomial model
library(pscl)  # hurdle model for handling excess zero counts
library(splm)  # spatial panal data model package


#####scatter plot
setwd("D:/Geodawksp/keypoly2")
kw.map <- readShapePoly("keywordpolygon22.shp")
kw.nb <- poly2nb(kw.map)
kw.tc <- kw.map$tc
kw.listw <- nb2listw(kw.nb)
tc.mc <- moran.test(kw.tc,kw.listw)
dpi <- 300
png("crime.lisa.png", width = 6.67*dpi, height = 6.67*dpi, res = dpi)
moran.plot(kw.tc, kw.listw, xlim = c(-750, 1500), ylim = c(-200, 400), xlab = "Totoal citation counts",
           ylab = "Spatially lagged total citation clounts", main = "Moran's I = 0.03676")
dev.off()



  