library(data.table)
library(dplyr)
library(httr)
library(xml2)
library(rvest)
library(stringr)



extract_html <- function(url) {
  print(url)
  sfc <- read_html(GET(url, config = config(ssl_verifypeer = FALSE))) # cainfo for certificate parameter
  
  return(sfc);
}


extract_page_info <- function(sfc) {
  cases_count <- sfc %>%
    html_nodes(".pagedisplay") %>%
    html_text() %>%
    str_extract_all("\\d+") %>%
    unlist() %>%
    as.numeric()
  
  return(cases_count);
}


extract_table <- function(sfc) {
  table <- sfc %>%
    html_nodes("table") %>%
    .[[1]] %>%
    html_table() %>%
    data.table()
  
  table <- format_table(table)
  
  return(table);
}


format_table <- function(table) {
  names(table) <- table[1,] %>%
    unlist() %>%
    as.character()
  table <- table[-1,]
  table$`Company/Name` <- str_split(table$`Company/Name`, "(\r|\n|\t)+")
  
  return(table);
}



# http://www.sfc.hk/edistributionWeb/gateway/EN/news-and-announcements/news/enforcement-news/?year=2020&month=1
url <- "http://www.sfc.hk/edistributionWeb/gateway/EN/news-and-announcements/news/enforcement-news/"
home_html <- extract_html(url)
months <- home_html %>%
  html_nodes("#monthMenu option") %>%
  html_attr("value") %>%
  .[-1]
years <- home_html %>%
  html_nodes("#yearMenu option") %>%
  html_text()
ym <- expand.grid(months, years) %>%
  data.table() %>%
  .[, c("Var1", "Var2") := .(Var2, Var1)] %>%
  rename(year = Var1, month = Var2)
urls <- paste0(url, "?year=", ym$year, "&month=", ym$month) %>%
  tail()

page_html <- urls %>%
  lapply(extract_html)
table <- page_html %>%
  lapply(extract_table)
page_info <- page_html %>%
  lapply(extract_page_info)
sfc <- data.table(urls, ym, page_html, table, page_info)
