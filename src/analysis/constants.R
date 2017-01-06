# Constants
METRIC.GROUPS <- data.frame(
  "group" = c(
    "Effectiveness","Effectiveness","Effectiveness","Effectiveness",
    "Effectiveness","Effectiveness","Effectiveness","Effectiveness",
    "Effectiveness","Performance","Performance","Performance","Performance",
    "Performance","Performance","Performance","Performance","Performance"
  ),
  "metric" = c(
    "Accuracy","Confusion Matrix","F-value","False Negative Rate (FNR)",
    "False Positive Rate (FPR)","Precision","Recall",
    "Receiver Operating Characteristic (ROC)","True Negative Rate (TNR)",
    "Computational Time","CPU Usage","Energy Consumption","Memory Usage",
    "Saved Battery","Scalability","Scanning Time","Slowdown","Throughput"
  )
)
METRIC.GROUPS$group <- factor(
  METRIC.GROUPS$group, levels = c("Effectiveness","Performance")
)

ADJUSTMENT.FACTORS <- data.frame(
  "metric" = c(
    "Accuracy","Confusion Matrix","F-value","False Negative Rate (FNR)",
    "False Positive Rate (FPR)","Precision","Recall",
    "Receiver Operating Characteristic (ROC)","True Negative Rate (TNR)",
    "Computational Time","CPU Usage","Energy Consumption","Memory Usage",
    "Scanning Time","Slowdown","Throughput"
  ),
  "adjustmentfactor" = c(
    10/41,8/21,3/24,12/22,21/34,9/26,13/39,13/23,8/21,7/28,5/22,4/25,4/43,7/20,
    8/36,8/30
  )
)
