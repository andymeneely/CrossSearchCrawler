source("constants.R")

init.libraries <- function(){
  suppressPackageStartupMessages(library("DBI"))
  suppressPackageStartupMessages(library("dplyr"))
  suppressPackageStartupMessages(library("ggplot2"))
  suppressPackageStartupMessages(library("grid"))
  suppressPackageStartupMessages(library("gridExtra"))
  suppressPackageStartupMessages(library("irr"))
  suppressPackageStartupMessages(library("reshape2"))
  suppressPackageStartupMessages(library("VennDiagram"))
}

get.theme <- function(){
  plot.theme <-
    theme_bw() +
    theme(
      plot.title = element_text(
        size = 14, face = "bold", margin = margin(5,0,25,0)
      ),
      axis.text.x = element_text(size = 10, angle = 50, vjust = 1, hjust = 1),
      axis.title.x = element_text(face = "bold", margin = margin(15,0,5,0)),
      axis.text.y = element_text(size = 10),
      axis.title.y = element_text(face = "bold", margin = margin(0,15,0,5)),
      strip.text.x = element_text(size = 10, face = "bold"),
      legend.position = "bottom",
      legend.title = element_text(size = 9, face = "bold"),
      legend.text = element_text(size = 9)
    )
  return(plot.theme)
}

db.connect <- function(host, port, user, password, dbname, provider){
  connection <- NULL

  if(provider == "PostgreSQL"){
    library("RPostgreSQL")
    driver <- dbDriver(provider)
    connection <- dbConnect(
      driver, host=host, port=port, user=user, password=password, dbname=dbname
    )
  } else if(provider == "MySQL"){
    library("RMySQL")
    driver <- dbDriver(provider)
    connection <- dbConnect(
      driver, host=host, port=port, user=user, password=password, dbname=dbname
    )
  } else if(provider == "SQLite"){
    library("RSQLite")
    driver <- dbDriver(provider)
    connection <- dbConnect(driver, dbname=dbname)
  } else {
    # TODO: Add other providers
    stop(sprint("Database provider %s not supported.", provider))
  }

  return(connection)
}

db.disconnect <- function(connection){
  return(dbDisconnect(connection))
}

db.get.data <- function(connection, query){
  return(dbGetQuery(connection, query))
}
