import pickle

# 保存したモデルを読み込む
model_outcome_e_e = pickle.load(open('outcome_e_e_rf_model.pkl', 'rb'))
model_hospitalstay_e_e = pickle.load(open('hospitalstay_e_e_rf_model.pkl', 'rb'))
model_nursingcare_apply_e = pickle.load(open('nursingcare_apply_e_rf_model.pkl', 'rb'))
model_outcome_e_g = pickle.load(open('outcome_e_g_rf_model.pkl', 'rb'))
model_hospitalstay_e_g = pickle.load(open('hospitalstay_e_g_rf_model.pkl', 'rb'))
model_outcome_e_o = pickle.load(open('outcome_e_o_rf_model.pkl', 'rb'))
model_hospitalstay_e_o = pickle.load(open('hospitalstay_e_o_rf_model.pkl', 'rb'))
model_outcome_p = pickle.load(open('outcome_p_rf_model.pkl', 'rb'))
model_hospitalstay_p = pickle.load(open('hospitalstay_p_rf_model.pkl', 'rb'))
model_nursingcare_apply_p = pickle.load(open('nursingcare_apply_p_rf_model.pkl', 'rb'))

# モデルを辞書にまとめる
models = {
    'outcome_e_e': model_outcome_e_e,
    'hospitalstay_e_e': model_hospitalstay_e_e,
    'nursingcare_e': model_nursingcare_apply_e,
    'outcome_e_g': model_outcome_e_g,
    'hospitalstay_e_g': model_hospitalstay_e_g,
    'outcome_e_o': model_outcome_e_o,
    'hospitalstay_e_o': model_hospitalstay_e_o,
    'outcome_p': model_outcome_p,
    'hospitalstay_p': model_hospitalstay_p,
    'nursingcare_p': model_nursingcare_apply_p  
}

