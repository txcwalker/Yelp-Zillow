# Yelp–Zillow Housing Price Prediction

## Table of Contents
1. [Abstract](#abstract)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Results](#results)
6. [Project Structure](#project-structure)
7. [Future Work](#future-work)
8. [Acknowledgments](#acknowledgments)

---

## Abstract
This project explores the relationship between local business activity and housing prices by integrating **Yelp API business data** with **Zillow housing data**. The primary objectives were:

- To investigate whether Yelp business metrics can serve as predictive features for housing prices.
- To build a **random forest regression model** to estimate housing prices using Yelp data.
- To analyze Yelp’s **search functionality** by reverse-engineering and comparing it to an engineered search algorithm.

The project demonstrates how publicly available business data can be leveraged for real estate analytics, while also uncovering potential biases in search algorithms.

---

## Features

### Yelp Data Integration
- Leveraged **Yelp API** to systematically extract and aggregate data on local businesses.

### Predictive Modeling
- Built a **random forest regression model** to estimate housing prices based on Yelp-derived features.
- Evaluated prediction accuracy by mapping results against Zillow’s housing price data.

### Search Algorithm Analysis
- Engineered a custom search algorithm to analyze, evaluate, and reverse-engineer Yelp’s search functionality.
- Compared results against Yelp’s native search to evaluate potential bias.

### Visualization
- Generated **heat density maps** to visualize geographic distribution of business activity and housing price predictions.
- Created summary plots highlighting the most common search results.
