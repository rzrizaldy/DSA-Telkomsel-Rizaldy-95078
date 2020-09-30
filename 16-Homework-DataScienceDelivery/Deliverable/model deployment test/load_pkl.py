# %%
from sklearn.externals import joblib
from utils.prepv1 import FeatureProcessor


# %%
clf = joblib.load("./XGB_SMOTE_v1.0_pkl.pkl")

#%%
columns = joblib.load("./X_columns_v1.0_pkl.pkl")

#%%
preprocessor = joblib.load("./preprocessor_v1.0_pkl.pkl")