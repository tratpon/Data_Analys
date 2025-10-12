from flask import Flask, request, render_template, send_file
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

COLUMNS = [
    "fixed acidity","volatile acidity","citric acid","residual sugar","chlorides",
    "free sulfur dioxide","total sulfur dioxide","density","pH","sulphates","alcohol","quality"
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = {col: [] for col in COLUMNS}
        num_rows = len(request.form.getlist(COLUMNS[0]))
        for col in COLUMNS:
            values = request.form.getlist(col)
            for i in range(num_rows):
                data[col].append(values[i])

        df = pd.DataFrame(data)
        for col in COLUMNS:
            df[col] = pd.to_numeric(df[col], errors='ignore')

        out_path = os.path.join(UPLOAD_FOLDER, "wine_input.xlsx")
        df.to_excel(out_path, index=False)
        return send_file(out_path, as_attachment=True)

    return render_template("index.html", columns=COLUMNS)

@app.route("/tutorial")
def tutorial():
    return render_template("tutorial.html", columns=COLUMNS)
if __name__ == "__main__":
    app.run(debug=True)
