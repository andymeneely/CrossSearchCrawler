# Clear
rm(list = ls())
cat("\014")

# Include Libraries
source("includes.R")

# Initialize Libraries
init.libraries()

directory <- "./data/irr/"
files <- list.files(path = directory, pattern = "*.csv")

reliability <- data.frame()
for(file in files){
  ratings <- read.csv(paste(directory, file, sep = ""), header = F)
  irr <- kappa2(ratings)
  reliability <- rbind(
    reliability,
    data.frame("file" = file, "kappa" = irr$value, "p" = irr$p.value)
  )
}
