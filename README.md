# Yelp–Zillow Housing Price Prediction

## Table of Contents
1. [Abstract](#abstract)
2. [Features](#features)
3. [Results](#results)
4. [Future Work](#future-work)
5. [Acknowledgments](#acknowledgments)
6. [Website](#website)

---

## Abstract
This project explores the relationship between local business activity and housing prices by combining **Yelp API business data** with **Zillow housing data**. The primary objectives were:

- To test whether Yelp business metrics can help predict housing prices.
- To build a **random forest regression model** that uses Yelp data as features.
- To reverse-engineer and compare Yelp’s **search functionality** against an engineered search algorithm.

This project shows how public business data can be applied to real estate analytics while also highlighting potential biases in search algorithms.

---

## Features

- **Yelp Data Integration**: Extracted and aggregated business data from Yelp’s API.  
- **Predictive Modeling**: Built a random forest regression model to estimate housing prices and mapped results for evaluation.  
- **Search Algorithm Analysis**: Designed and tested a custom search algorithm against Yelp’s version to explore bias.  
- **Visualization**: Created heat density maps and tag graphs to summarize and display geographic patterns.  

---

## Results
- The **random forest model** demonstrated promising predictive ability for housing price estimation.  
- The **search bias analysis** revealed measurable differences between the engineered and Yelp algorithms.  
- Visual outputs (heat maps, graphs) revealed clear spatial patterns in business activity and housing prices.  

---

## Future Work
- Test alternative machine learning models (e.g., gradient boosting, XGBoost).  
- Expand coverage to additional cities and states.  
- Explore causality between business density and housing market trends.  
- Incorporate other public datasets such as Census or Google Places data.  

---

## Acknowledgments
- **Yelp API** for business data.  
- **Zillow** for housing datasets.  
- Libraries: `scikit-learn`, `pandas`, `matplotlib`, `seaborn`, `geopandas`.  

---

## Website
This project is also showcased on my personal website with write-ups and visualizations:  
[Visit the Project Page](https://txcwalker.github.io)
