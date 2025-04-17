from automationdashboard import app
from flask import jsonify

@app.route('/healthcheck')
def healthcheck():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

def main():
    """Main entry point"""
    app.run(debug=True, host='0.0.0.0', port=9098)

if __name__ == '__main__':
    main()