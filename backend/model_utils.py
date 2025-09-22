import joblib, numpy as np
from features import extract_basic_features
from scipy.sparse import hstack

MODEL_PATH = "model.joblib"
bundle = joblib.load(MODEL_PATH)
MODEL, VECT, FEAT_NAMES = bundle['model'], bundle['vectorizer'], bundle['basic_feature_names']

def predict_url(url: str):
    basic = extract_basic_features(url)
    basic_values = [basic[k] for k in FEAT_NAMES]
    from scipy import sparse
    X_text = VECT.transform([url])
    X_basic = sparse.csr_matrix(np.array(basic_values).reshape(1,-1))
    X = hstack([X_text, X_basic])
    score = float(MODEL.predict_proba(X)[:,1][0])
    return score, basic

