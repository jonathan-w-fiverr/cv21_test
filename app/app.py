import numpy as np
import pandas as pd
import pickle

from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)
CORS(app)

gigs_dataset = pd.read_csv("in/gigs_dataset.csv")
tfidf = pickle.load(open("in/tfidf_tags_transformer.pickle", "rb"))
gigs_tfidf = pickle.load(open("in/gigs_tags_tfidf.pickle", "rb"))

@app.route("/")
def hello_world():
    return "<p>Hello, Hackers!</p>"

@app.route('/get_gigs_by_skills', methods=['POST'])
def predict():
    data = request.get_json()
    skills = data.get("skills")
    text = ", ".join([str(i) for i in skills])

    gigs = get_related_gigs_prod(gigs_dataset, tfidf, gigs_tfidf, text, thresh=0.2)
    print("RESULT:", gigs)
    preds = [{"category": cat, "gigIds": ids} for cat, ids in gigs.items()]
    return jsonify(preds)

def get_related_gigs_prod(gigs_dataset, tfidf, gigs_tfidf, text, thresh=0.2):
    cv_tfidf = tfidf.transform([text])
    res = gigs_tfidf.dot(cv_tfidf.T)
    res_indx = [indx for indx in np.argsort(res.toarray().squeeze())[-10:]
                if res[indx > thresh]]
    res_dict = {}
    for indx in res_indx:
        if gigs_dataset.iloc[indx]['sub_category_name'] not in res_dict:
            res_dict[gigs_dataset.iloc[indx]['sub_category_name']] = []
        res_dict[gigs_dataset.iloc[indx]['sub_category_name']].append(int(gigs_dataset.iloc[indx]['gig_id']))
    return res_dict

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
