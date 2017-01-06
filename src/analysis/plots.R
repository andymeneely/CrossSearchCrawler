# Clear
rm(list = ls())
cat("\014")

# Include Libraries
source("includes.R")

# Initialize Libraries
init.libraries()

##########################################
### Query Data
##########################################
query <- "SELECT p.year, s.metric
          FROM publications p
            JOIN searchpublink spl ON spl.pubid = p.id
            JOIN searches s ON spl.searchid = s.id
          WHERE p.year <> '' AND s.metric <> '(Tagged papers)'
          ORDER BY s.metric, p.year"

connection <- db.connect(dbname = "data/searches.db", provider = "SQLite")
dataset <- db.get.data(connection, query) %>%
  mutate(
    metric = as.factor(metric), year = as.numeric(year)
  ) %>%
  inner_join(., METRIC.GROUPS, by = "metric")
dataset$metric <- factor(dataset$metric, levels = levels(METRIC.GROUPS$metric))
db.disconnect(connection)

dataset.grouped.year <- dataset %>%
  group_by(year) %>%
  summarize(count.per.year = n())

##########################################
### Usage: Bar Plots
##########################################

# Prepare Data Set
plot.dataset <- dataset %>%
  group_by(group, metric) %>%
  summarise(count = n()) %>%
  inner_join(., ADJUSTMENT.FACTORS, by = "metric") %>%
  mutate(count = round(count * adjustmentfactor)) %>%
  select(group, metric, count) %>%
  arrange(group, -count)

plot.dataset$metric <- factor(
  plot.dataset$metric, levels = plot.dataset$metric
)

# Export Resolution: 900 x 600
ggplot(plot.dataset, aes(x = metric, y = count)) +
  geom_bar(
    stat = "identity", width = 0.7, position = "dodge", fill = "#8ebec8"
  ) +
  geom_text(aes(label = paste(" ", count, " ")), vjust = "inward") +
  facet_grid(. ~ group, scales = "free", space = "free") +
  labs(
    title = "Frequency of Use of IDS Evaluation Metrics",
    x = "Metric", y = "Number of Relevant Papers"
  ) +
  get.theme()

##########################################
### Evolution: Distribution of Papers
##########################################

# Prepare Data Set
plot.dataset <- dataset.grouped.year

# Export Resolution: 600 x 400
ggplot(plot.dataset, aes(x = year, y = count.per.year)) +
  geom_area(stat = "identity", fill = "#8ebec8") +
  scale_x_continuous(
    breaks = seq(min(plot.dataset$year), max(plot.dataset$year), by = 4)
  ) +
  labs(
    title = "Distribution of Number of Primary IDS Studies By Year",
    x = "Year", y = "Number of Primary Studies"
  ) +
  get.theme()

##########################################
### Evolution: Area Plots
##########################################

# Prepare Data Set
plot.dataset <- dataset %>%
  group_by(group, metric, year) %>%
  summarise(count = n()) %>%
  inner_join(., ADJUSTMENT.FACTORS, by = "metric") %>%
  inner_join(., dataset.grouped.year, by = "year") %>%
  mutate(count = (count * adjustmentfactor)) %>%
  mutate(percent = count / count.per.year) %>%
  select(group, metric, year, count, count.per.year, percent) %>%
  arrange(group, metric)

plot.dataset <- plot.dataset %>%
  filter(year >= 2002)

plot.dataset$metric <- factor(
  plot.dataset$metric, levels = unique(plot.dataset$metric)
)

# Export Resolution: 1200 x 900
ggplot(plot.dataset, aes(x = year, y = percent)) +
  geom_line(stat = "identity", size = 0.8) +
  scale_y_continuous(labels = scales::percent) +
  scale_x_continuous(
    breaks = seq(min(plot.dataset$year), max(plot.dataset$year), by = 2)
  ) +
  facet_wrap(~ metric, ncol = 4) +
  labs(
    title = "Evolution of Use of IDS Evaluation Metrics",
    x = "Year", y = "Proportion of Relevant Papers"
  ) +
  get.theme()

##########################################
### Venn Diagrams
##########################################

# Precision vs Recall
## Export Resolution: 460 x 300
grid.newpage()
plot.venn <- draw.pairwise.venn(
  865, 982, 499, category = c("Precision or FPR", "Recall or FNR"),
  alpha = rep(0.3, 2), fill = c("#ff7f0e", "#2ca02c"), lty = "blank",
  fontfamily = rep("sans", 3), cat.pos = c(210, 145), cat.dist = c(0.05, 0.05),
  cat.fontfamily = rep("sans", 2), cat.fontface = rep("bold", 2), cex = 0.8
)
grid.draw(plot.venn)

# Computational Time vs Memory
## Export Resolution: 460 x 300
grid.newpage()
plot.venn <- draw.pairwise.venn(
  162, 255, 11, category = c("Computational Time", "Memory Usage"),
  fill = c("#ff7f0e", "#2ca02c"), lty = "blank", alpha = rep(0.3, 2),
  fontfamily = rep("sans", 3), cat.pos = c(195, 155), cat.dist = c(0.05, 0.07),
  cat.fontfamily = rep("sans", 2), cat.fontface = rep("bold", 2), cex = 0.8,
  ext.text = F
)
grid.draw(plot.venn)

# Effectiveness vs Performance
## Export Resolution: 460 x 300
grid.newpage()
plot.venn <- draw.pairwise.venn(
  1172, 767, 287, category = c("Effectiveness", "Performance"),
  fill = c("#ff7f0e", "#2ca02c"), lty = "blank", alpha = rep(0.3, 2),
  fontfamily = rep("sans", 3), cat.pos = c(330, 27), cat.dist = c(0.05, 0.07),
  cat.fontfamily = rep("sans", 2), cat.fontface = rep("bold", 2), cex = 0.8
)
grid.draw(plot.venn)
