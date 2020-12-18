import greek_cnn

from flask import Flask, request

app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    post_content = request.get_json()
    prediction = greek_cnn.predict(post_content)
    return {"prediction": prediction}


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
