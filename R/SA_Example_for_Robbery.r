#setwd("D:/Geodawksp/keypoly2")
#setwd("D:/Geodawksp/exmaple")
library(spdep)
library(maptools)  #readShapePoly
library(geoR)   #boxcocfit
library(MASS)  # negative binomial model
library(pscl)  # hurdle model for handling excess zero counts
library(splm)  # spatial panal data model package

# kw.map <- readShapePoly("keywordpolygons22.shp")
# plot(kw.map, col = kw.map$y2010)
# n <- length(kw.map)
# 
# kw.tc <- kw.map$tc
# kw.stc <- kw.map$stc
# kw.2010 <- kw.map$y2010
# #count zero in kw.2010
# zc.2010 <- 0
# for (i in 1:n){
#   if(kw.2010[i]==0)
#     zc.2010 <- zc.2010+1
# }
# 
# kwr.2010 <- kw.2010/sum(kw.2010)
# hist(kwr.2010)
# shapiro.test(kwr.2010)
# # conduct boxcox transformation
# bc.kwr2010 <- boxcoxfit(kwr.2010, lambda = 1, lambda2 = TRUE)
# summary(bc.kwr2010)
# lmd <- bc.kwr2010$lambda[1]
# lmd2 <- bc.kwr2010$lambda[2]
# bc_kwr2010 <- ((kwr.2010+lmd2)^lmd-1)/lmd
# shapiro.test(bc_kwr2010)
# 
# # both the regulized data and the transformed data fail to conform to a normal distribution,
# # so a possion model for the count data will be employed
# ps.kw2010 <- glm(kw.2010 ~  kw.stc + kw.tc + 1, family = poisson(link = log))
# summary(ps.kw2010)
# # p value of goodness of fit
# pchisq(ps.kw2010$deviance, df=ps.kw2010$df.residual, lower.tail = FALSE)
# 
# # overdispersion is tested in the poisson model, so turn to the negative binomial model
# #glm.nb is in library MAss
# nb.kw2010 <- glm.nb(kw.2010 ~ kw.tc + 1)
# summary(nb.kw2010)
# 
# # negative binomial model does not work either, so turn to hurdle model to handle excess zeros
# hd.kw2010 <- hurdle(kw.2010 ~ kw.tc, dist = "negbin")
# summary(hd.kw2010)


#####scatter plot
# kw.map <- readShapePoly("Sanfran_crime.shp")
# kw.nb <- poly2nb(kw.map)
# kw.tc <- kw.map$tc
# kw.listw <- nb2listw(kw.nb)
# tc.mc <- moran.test(kw.tc,kw.listw)
# dpi <- 300
# png("crime.lisa.png", width = 6.67*dpi, height = 6.67*dpi, res = dpi)
# moran.plot(kw.tc, kw.listw, xlim = c(-750, 1500), ylim = c(-200, 400), xlab = "Totoal citation counts", 
#            ylab = "Spatially lagged total citation clounts", main = "Moran's I = 0.03676")
# dev.off()

setwd("D:/publications/GitWksp/Shapefiles/exmaple")
sanfran <- readShapePoly("Sanfran_crime.shp")
plot(sanfran)
sf.nb <- poly2nb(sanfran, queen = FALSE)
sf.listw <- nb2listw(sf.nb, zero.policy = TRUE)
rb <- sanfran$robbery
rb.mc <- moran.test(rb,sf.listw, zero.policy = TRUE)
rb.mc
moran.plot(rb, sf.listw, zero.policy = TRUE, xlim = c(-30, 120), ylim = c(-30, 80))
dpi <- 300
png("rb.lisa.png", width = 6.67*dpi, height = 6.67*dpi, res = dpi)
moran.plot(rb, sf.listw, zero.policy = TRUE, xlim = c(-30, 120), ylim = c(-30, 80), xlab = "Robbery counts", 
           ylab = "Spatially lagged robbery counts", main = "Moran's I = 0.5577")
dev.off()


  