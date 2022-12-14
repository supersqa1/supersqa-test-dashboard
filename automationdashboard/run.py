
from automationdashboard import app







@app.route('/healthcheck', methods=["GET"])
def healthCheck():
    return "OK"


if __name__ == '__main__':

    app.run(debug=True, port=9098)