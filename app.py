from flask import Flask, render_template, url_for, request, jsonify
import ejemplo as ej
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/query', methods=['GET'])
def query():
    input_value = request.args.get('input', '') 
    res = ej.distance_one(input_value)
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True)