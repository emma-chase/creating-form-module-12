import flask
from flask import request, render_template, redirect, url_for
from flask_cors import CORS
import requests


app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "seasdad(*2sffcra01^23sdet"

CORS(app)

# Get this URL from the Azure Overview page of your API web app
api_url = "https://new-elchase-api-drhed6h2ajawgwcv.eastus-01.azurewebsites.net"  # base url for API endpoints


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        form = request.form

        # Extract form fields
        age = form.get("age")
        gender = form.get("gender")
        country = form.get("country")
        highest_deg = form.get("highest_deg")
        coding_exp = form.get("coding_exp")
        title = form.get("title")
        company_size = form.get("company_size")

        # Server-side validation
        required_fields = {
            "age": age,
            "gender": gender,
            "country": country,
            "highest_deg": highest_deg,
            "coding_exp": coding_exp,
            "title": title,
            "company_size": company_size,
        }

        # Find missing fields
        missing = [field for field, value in required_fields.items() if not value]

        if missing:
            error_message = "Please fill out all required fields: " + ", ".join(missing)
            return render_template("index.html", error=error_message, form_data=form)

        # Proceed if all fields are filled
        salary_predict_variables = {
            "age": age,
            "gender": gender,
            "country": country,
            "highest_deg": highest_deg,
            "coding_exp": coding_exp,
            "title": title,
            "company_size": company_size,
        }

        url = api_url + f"/predict"
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(url, json=salary_predict_variables, headers=headers)

            if response.status_code == 200:
                prediction = response.json()
                return render_template("index.html", prediction=prediction)
            else:
                error_message = f"Failed to get prediction, server responded with status code: {response.status_code}"
                return render_template("index.html", error=error_message)

        except requests.exceptions.RequestException as e:
            return render_template("index.html", error="Failed to make request to prediction API.")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)