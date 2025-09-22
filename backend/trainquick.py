import pandas as pd, joblib, numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from scipy.sparse import hstack
from features import extract_basic_features

df = pd.read_csv("data/labeled_urls.csv")

basic_feats = df['url'].apply(lambda u: pd.Series(extract_basic_features(u)))
tf = TfidfVectorizer(analyzer='char_wb', ngram_range=(3,6), max_features=2000)
X_text = tf.fit_transform(df['url'])
X_basic = basic_feats.fillna(0).values
X = hstack([X_text, X_basic])
y = df['label'].values

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=42)
clf = LogisticRegression(max_iter=1000).fit(X_train,y_train)

print(classification_report(y_test, clf.predict(X_test)))
print("AUC:", roc_auc_score(y_test, clf.predict_proba(X_test)[:,1]))

joblib.dump({"model":clf,"vectorizer":tf,"basic_feature_names":list(basic_feats.columns)},"model.joblib")
print("Saved model.joblib")

