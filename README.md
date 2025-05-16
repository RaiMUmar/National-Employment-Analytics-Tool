# Job Market Insights: Canada

A Python-based data visualization tool that explores the relationship between job vacancies, education levels, and income across Canadian provinces. The tool provides insights into provincial trends by reading, cleaning, and merging government datasets (CSV format), and rendering visual correlations using `matplotlib`.

---

## 📊 Features

- **Job Market Trends**: Line chart showing monthly job vacancies across provinces.
- **Education vs. Employment Vacancies**: Scatter plot correlating tertiary education percentages with average job vacancies.
- **Income vs. Education**: Scatter plot showing average income (ages 25–34) vs. education rate by province.

---

## 📂 Data Inputs

You will need the following CSV files:

- `data.csv`: Contains job vacancy data per province/month.
- `education.csv`: Contains tertiary education percentages by province.
- `income.csv`: Average income by age group and province.

Ensure the headers and formats match those expected by the script (skip rows and footer patterns already handled in the code).

---

## 🛠 How to Run

Run the script from your terminal:

```bash
python3 jobVacancies.py
```

You’ll be presented with a menu:

```
1) Job Market Trends & Demand (Line Chart)
2) Education vs. Employment Vacancies
3) Income vs. Education (by Age Group)
4) Show ALL
Q) Quit
```

---

## 📅 Last Updated
March 26, 2025

---

## 📦 Requirements

- Python 3.x
- pandas
- matplotlib

Install required packages with:

```bash
pip install pandas matplotlib
```

---

## 🧠 Highlights

- Uses custom standardization to align inconsistent province naming across datasets
- Forward-fills missing rows and coerces non-numeric values for clean plotting
- Helps users explore regional gaps between education levels, job opportunities, and earning power

---

## 📄 License

This project is free and open-source under the MIT License.
