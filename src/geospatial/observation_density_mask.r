library(graphics) 	# for persp
library(MASS) 		# for kde2d
library(ggplot2) 	# for ggplot
library(raster)
library(fields) 	# for thin plate spline functionality

#' Create a 1/0 raster mask for use with clipping regions relative to observation point density
#'
#' @param xy An xy data list
#' @param std_dev_scalar The scalar by which to multiple the observation density standard deviation, which is then used to threshold the mask (deafult = 2)
#' @param plotting A boolean option for creating plots as the function runs (deafult = TRUE)
#' @examples
#' x<-c(1,2,3,4)
#' y<-c(1,2,3,4)
#' xy<-cbind(x,y)
#' obs_mask<-observation_density_mask(xy, std_dev_scalar=2)
observation_density_mask <- function(xy, std_dev_scalar=2, plotting=TRUE){
	dens <- kde2d(xy[,1], xy[,2])

	if(plotting==TRUE){
		x11()
		persp(dens, phi = 30, theta = 20, d = 5, main = "Density surface")
	}

	densdf <- data.frame(expand.grid(x = dens$x, y = dens$y), density = as.vector(dens$z))

	#if(plotting==TRUE){
	#	x11()
	#	ggplot(densdf,aes(x=densdf[,1],y=densdf[,2],color=densdf[,3]))+geom_point(size=5)
	#}

	#interp the density function to grid 
	densdf_fit<-Tps(densdf[,1:2],densdf[,3]) # thin plate spline fit - hits an error if too many points (subsample input if this is the case)

	densdf_coords<-densdf[,1:2]

	densdf_xg<-make.surface.grid(fields.x.to.grid(densdf_coords)) # makes a mesh grid of x and y

	densdf_fhat<- predict(densdf_fit, densdf_xg) # indexes values of based on the thin plate spline to their xy index locations (i.e. this is 1d and is therefore a length of the dimensions of plot(xg))

	densdf_out.p<- as.surface(densdf_xg, densdf_fhat) # creates a surface from predictions onto the xy mesh points (xg), components of which can be called as out.p$x (cols), out.p$y (rows), out.p$z (z value) etc...

	if(plotting==TRUE){
		x11()
		surface(densdf_out.p)
	}

	density_rst<-raster(densdf_out.p) # density raster

	#create 1/0 version
	density_std_dev<-cellStats(density_rst, stat='sd')

	threshold_density<-(density_std_dev*std_dev_scalar) # ALTER THRESHOLD - larger value gives a tighter crop

	if(threshold_density>density_rst@data@max){
		stop("Smaller scalar (std_dev_scalar) required - threshold density > than largest value on density grid")
	}

	density_rst[density_rst<threshold_density]<-0
	density_rst[is.na(density_rst)]<-0
	density_rst[density_rst>=threshold_density]<-1

	if(plotting==TRUE){
		x11()
		persp(density_rst, phi = 30, theta = 20, d = 5, main = "1/0 density surface") # 3d plot of density
	}

	return(density_rst)

}

