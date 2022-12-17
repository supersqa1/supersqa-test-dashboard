from automationdashboard import app

from flask import render_template
from automationdashboard.src.test_results_processor import TestResultsProcessor




@app.route('/')
def home():
    """
    Home page
    """

    results_processor = TestResultsProcessor()
    final_data = results_processor.get_all_results_formatted()

    return render_template("home.html", result_rows=final_data)

