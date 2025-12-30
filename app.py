from flask import Flask, render_template, request
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    total_sales = None
    category_sales = None
    chart_path = None

    if request.method == "POST":
        file = request.files.get("file")
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            # Read CSV
            df = pd.read_csv(filepath)
            df["Date"] = pd.to_datetime(df["Date"])

            # Calculations
            total_sales = df["Amount"].sum()
            category_sales = df.groupby("Category")["Amount"].sum()

            daily_sales = df.groupby("Date")["Amount"].sum().reset_index()

            # -------- BAR CHART (COLORFUL) --------
            sns.set_theme(style="whitegrid")
            plt.figure(figsize=(8, 4))

            plt.bar(
                daily_sales["Date"].astype(str),
                daily_sales["Amount"],
                color=sns.color_palette("viridis", len(daily_sales))
            )

            plt.title("Daily Sales Trend", fontsize=14, weight="bold")
            plt.xlabel("Date")
            plt.ylabel("Sales Amount")
            plt.xticks(rotation=45)

            plt.tight_layout()

            chart_path = "static/sales_chart.png"
            plt.savefig(chart_path)
            plt.close()
            # -------------------------------------

    return render_template(
        "index.html",
        total_sales=total_sales,
        category_sales=category_sales,
        chart_path=chart_path
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
