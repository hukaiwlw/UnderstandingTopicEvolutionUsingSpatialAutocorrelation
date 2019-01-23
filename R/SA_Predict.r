library(spdep)
library(maptools)  #readShapePoly
library(geoR)   #boxcocfit
library(MASS)  # negative binomial model
library(pscl)  # hurdle model for handling excess zero counts
library(splm)  # spatial panal data model package


#####scatter plot
setwd("D:/publications/GitWksp/Shapefiles/kypolyTop20")
kw.top20 <- readShapePoly("t20_poly")
t20.2010 <- kw.top20$y2010
t20.2013 <- kw.top20$y2013
t20.2016 <- kw.top20$y2016

kw.lm <- lm(t20.2016 ~ t20.2010 + t20.2013)
summary(kw.lm)
predict(kw.lm)

t20.nb <- poly2nb(kw.top20)
t20.listw <- nb2listw(t20.nb)

t20.lag <- lagsarlm(t20.2016 ~ t20.2010 + t20.2013, listw = t20.listw)
summary(t20.lag)
predict(t20.lag)