from flask import Flask, request, abort, jsonify

app = Flask(__name__)

@app.route('/add/<int:a>/<int:b>', methods=["GET"])
def add(a, b):
    try:
        return jsonify({'result (a+b)': a + b })
    except Exception as err:
        return jsonify({'message': str(err)}), 400

@app.route('/subs/<int:a>/<int:b>', methods=["GET"])
def subs(a, b):
    try:
        return jsonify({'result (a-b)': a - b })
    except Exception as err:
        return jsonify({'message': str(err)}), 400

@app.route('/multiply/<int:a>/<int:b>', methods=["GET"])
def multiply(a, b):
    try:
        return jsonify({'result (a*b)': a * b })
    except Exception as err:
        return jsonify({'message': str(err)}), 400

@app.route('/divise/<int:a>/<int:b>', methods=["GET"])
def divise(a, b):
    try:
        return jsonify({'result (a/b)': a / b })
    except Exception as err:
        return jsonify({'message': str(err)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)