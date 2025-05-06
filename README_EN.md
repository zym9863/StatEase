# StatEase - Simple Statistical Analysis Tool

English | [简体中文](README.md)

StatEase is a simple statistical analysis tool based on Python and Gradio, focusing on providing descriptive statistics functionality. This tool allows users to quickly obtain statistical analysis results by uploading datasets, manually entering data, or selecting example data.

## Features

- **Multiple Data Input Methods**:
  - Upload CSV files
  - Manually enter data
  - Select preset example data

- **Comprehensive Descriptive Statistics**:
  - Basic statistics (mean, median, standard deviation, etc.)
  - Distribution characteristics (skewness, kurtosis)
  - Outlier detection

- **Parameter Estimation**:
  - Point estimation (sample mean, sample proportion)
  - Interval estimation (confidence intervals for mean and proportion)
  - Selectable confidence levels (90%, 95%, 99%)

- **Data Visualization**:
  - Histogram (with kernel density estimation)
  - Box plot (with data point distribution)

## Installation and Running

### Local Execution

1. Clone or download this repository

2. Create and activate a virtual environment (recommended)
   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment (Windows)
   venv\Scripts\activate

   # Activate virtual environment (Linux/Mac)
   source venv/bin/activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application
   ```bash
   python app.py
   ```

5. Access the displayed URL in your browser (usually http://127.0.0.1:7860)

### Hugging Face Spaces Deployment

This project can be directly deployed to Hugging Face Spaces:

1. Create a new Space on Hugging Face
2. Select Gradio as the SDK
3. Upload project files
4. The Space will automatically install dependencies and start the application

## User Guide

### Upload Data

1. Switch to the "Upload Data" tab
2. Click the upload button to select a CSV file
3. Click the "Analyze" button to get results

### Manual Input

1. Switch to the "Manual Input" tab
2. Enter data in the text box, separated by commas, spaces, or line breaks
3. Click the "Analyze" button to get results

### Use Example Data

1. Switch to the "Example Data" tab
2. Select an example dataset from the dropdown menu
3. Click the "Analyze" button to get results

### Parameter Estimation

1. Switch to the "Parameter Estimation" tab
2. Enter data in the text box, separated by commas, spaces, or line breaks
3. Select the estimation type (mean estimation or proportion estimation)
4. Choose a confidence level (90%, 95%, or 99%)
5. If proportion estimation is selected, enter a threshold value (values greater than or equal to this are considered "successes")
6. Click the "Calculate Parameter Estimation" button to get results
