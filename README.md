# cyclistic-bike-share-analysis
End-to-end data analysis of Cyclistic bike-share trip data (12 months, 5.7M+ rides) — Excel, Python/pandas, and statistical analysis to inform a membership-conversion marketing strategy.
# 🚲 Cyclistic Bike-Share Analysis

**Business question:** How do annual members and casual riders use Cyclistic
bikes differently — and what should the marketing team do about it?

This is a complete, end-to-end data analytics case study: from raw trip data
to a stakeholder-ready report, a technical documentation trail, and an
executive presentation.

## 📊 Project Overview

| | |
|---|---|
| **Dataset** | 12 months of Cyclistic (Divvy) trip data, July 2025 – June 2026 |
| **Raw records** | ~6.4 million rides |
| **Cleaned records** | 5,764,564 valid rides analyzed |
| **Tools** | Excel (manual methodology build), Python/pandas (full automation) |
| **Deliverables** | Stakeholder report · Technical appendix · Executive presentation |

## 🔑 Key Findings

- **Ride duration:** Casual riders take longer trips (~19 min) but far less
  often than members (~12 min, more frequent).
- **Weekly timing:** Casual riders peak on weekends; members peak on
  weekdays — pointing to leisure vs. commuting usage.
- **Seasonality:** Casual ridership is far more weather-sensitive (-93% in
  winter vs. -75% for members).
- **Bike type:** Casual riders slightly favor electric bikes (69% vs. 66%).

## ✅ Recommendations

1. **Weekend membership offer** — target weekend usage patterns with an
   electric-bike incentive.
2. **Summer-timed campaign** — launch the core marketing push during the
   July–August usage peak.
3. **Peak-season availability review** — ensure bike supply at recreational
   stations doesn't undercut the conversion opportunity.

## 📁 Repository Structure
├── reports/ → Stakeholder report & technical appendix (PDF)
├── presentation/ → Executive summary deck (PDF)
├── scripts/ → Full Python cleaning & analysis pipeline
└── visuals/ → Supporting charts (PNG)

## 🛠️ Methodology

Data was first cleaned and validated manually in Excel for a subset of
months (to build and cross-check the cleaning logic), then the identical
methodology was automated in Python/pandas across the full 12-month dataset.
Full technical detail — formulas, validation checks, and issues encountered
and resolved — is documented in
[`reports/Cyclistic_Technical_Appendix_EN.pdf`](reports/Cyclistic_Technical_Appendix_EN.pdf).

Raw data source: [Divvy trip data](https://divvy-tripdata.s3.amazonaws.com/index.html),
provided by Motivate International Inc.

## 📄 Full Documentation

- 📘 [Stakeholder Report](reports/Cyclistic_Case_Study_Report_EN.pdf)
- 🔧 [Technical Appendix](reports/Cyclistic_Technical_Appendix_EN.pdf)
- 🎤 [Presentation Deck](presentation/Cyclistic_Presentation.pdf)
- 
## 📊 Key Visualizations

![Chart#1](visuals/chart%231.png)
![Chart#2](visuals/chart%232.png)
![Chart#3](visuals/chart%233.png)
---
*Prepared by Rayan Ibrahim | Data Analyst*
