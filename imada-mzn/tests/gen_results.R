rlib = "tests/rlib"
repo = c("http://rstudio.org/_packages", "http://cran.rstudio.com")

if(!require("data.table")){
    install.packages("data.table", repos=repo, dependencies=TRUE, lib=rlib)
    library(data.table)
}

if(!require("ggplot2")){
    install.packages("ggplot2", repos=repo, dependencies=TRUE, lib=rlib)
    library(ggplot2)
}


dat.files <- list.files("results/", pattern="*\\.csv")
for(f.name in dat.files) {
    splitted.name <- strsplit(f.name, "_")
    timelimit <- strsplit(splitted.name[[1]][3], "\\.")[[1]][1]
    dat <- read.csv(paste("results/", f.name, sep=""), na.strings=c("", "NA"))
    #dat
    # Average results and violations of all runs for each method
    dat <- data.table(dat, key="Solver")
    dat <- dat[, list(Time=mean(Time)), by=list(Model, Solver, Obj, State)]
    dat

    dat.feas <- dat[(as.character(dat$State)=="feas"),]
    unknown.dat <- dat[(as.character(dat$State)=="unknown"),]

    obj.time.plot <- ggplot(data=dat.feas, aes(x=Time, y=Obj, color=Solver)) +
        geom_line() + 
        geom_point() +
        scale_y_continuous(name="Value of the Objective function", breaks=seq(0, 2500, 50), labels=seq(0, 2500, 50)) +
        scale_x_continuous(name="Average Time (seconds)", breaks=seq(0, as.integer(timelimit), 50), labels=seq(0,as.integer(timelimit), 50)) +
        ggtitle(paste("Value of the Objective Function over Time (Time limit =", timelimit, "seconds)"))
    ggsave(filename=paste("results/obj_time_", timelimit, ".pdf", sep=""), device='pdf', width=30, height=20, units="cm")
}



