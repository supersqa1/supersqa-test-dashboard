from automationdashboard import app

from flask import render_template
from automationdashboard.src.test_results import TestResults





@app.route('/')
def home():
    """
    Home page
    """

    results_helper = TestResults()
    final_data = results_helper.get_all_results_formatted()

    return render_template("home.html", result_rows=final_data)

