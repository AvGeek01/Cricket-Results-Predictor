# Cricket-Results-Predictor

A full-stack machine learning web application that predicts **cricket match winners**, **first innings scores**, and **live win probabilities** using multiple machine learning algorithms implemented entirely from scratch.

**Live Demo:** https://rish20.pythonanywhere.com/

---

## Overview

This project aims to predict cricket match outcomes using historical match data and key performance indicators. The application analyzes factors such as team rankings, recent form, toss decisions and match format to generate intelligent predictions for both pre-match and live match scenarios.

---

## Features

- Predicts the winning team before a match begins
- Predicts projected first innings score
- Live match prediction using runs, wickets, and overs
- Calculates win probabilities
- Ensemble prediction using multiple ML algorithms
- Responsive Flask-based web dashboard
- Historical cricket dataset with engineered features

---

## Machine Learning Algorithms

The following algorithms were implemented **from scratch**, without using machine learning libraries:

- Logistic Regression
- K-Nearest Neighbors (KNN)
- Decision Tree
- Naive Bayes
- Perceptron
- Weighted Ensemble Voting

---

## Features Used

The prediction models consider multiple match attributes, including:

- Team 1
- Team 2
- Toss Winner
- Toss Decision
- Match Format (T20 / ODI)
- Team Rankings
- Recent Team Form
- Rank Differential
- Team Strength Encoding

---

## Dataset

The model is trained on a structured historical cricket dataset containing information such as:

- Teams
- Match Format
- Toss Winner
- Toss Decision
- Team Rankings
- Recent Form
- Match Winner

The dataset is divided using a **5-part split**, with **80% used for training** and **20% reserved for testing** to ensure reliable evaluation and minimize overfitting.

---

## Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask

### Machine Learning
- Custom Machine Learning Algorithms (No ML Libraries)

---

## Project Structure

```text
Cricket-Match-Predictor/
│
├── app.py
├── project.py
├── cricket_dataset.csv
├── train.csv
├── test.csv
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   ├── script.js
│   └── assets/
│
└── README.md
```

---

This project is intended for educational and research purposes.
