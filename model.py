import pickle
import gzip

# 圧縮されたモデルを読み込む関数
def load_compressed_model(file_path):
    with gzip.open(file_path, 'rb') as f:
        return pickle.load(f)

# 保存したモデルを読み込む
model_outcome_e = load_compressed_model('outcome_e_rf_model.pkl.gz')
model_hospitalstay_e = load_compressed_model('hospitalstay_e_rf_model.pkl.gz')
model_nursingcare_apply_e = load_compressed_model('nursingcare_apply_e_rf_model.pkl.gz')
model_outcome_p = load_compressed_model('outcome_p_rf_model.pkl.gz')
model_hospitalstay_p = load_compressed_model('hospitalstay_p_rf_model.pkl.gz')
model_nursingcare_apply_p = load_compressed_model('nursingcare_apply_p_rf_model.pkl.gz')

# モデルを辞書にまとめる
models = {
    'outcome_e': model_outcome_e,
    'hospitalstay_e': model_hospitalstay_e,
    'nursingcare_e': model_nursingcare_apply_e,
    'outcome_p': model_outcome_p,
    'hospitalstay_p': model_hospitalstay_p,
    'nursingcare_p': model_nursingcare_apply_p  
}
