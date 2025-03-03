import pandas as pd
import numpy as np
import pickle
from model import models  # model.pyからモデルをインポート

def make_predictions(input_array):

    # 予定外_1 の値に応じて使用するモデルを切り替える
    if input_array[0][16] == 0:  # 予定外_1
        prediction_outcome = models['outcome_p'].predict(input_array)
        probabilities_outcome = models['outcome_p'].predict_proba(input_array)
        prediction_hospitalstay = models['hospitalstay_p'].predict(input_array)
        probabilities_hospitalstay = models['hospitalstay_p'].predict_proba(input_array)
    else:
        if input_array[0][17] == 1:  # 診療科_救命科
            model_key = 'e_e'
        elif input_array[0][18] == 1:  # 診療科_消化器内科
            model_key = 'e_g'
        else:
            model_key = 'e_o'
        prediction_outcome = models[f'outcome_{model_key}'].predict(input_array)
        probabilities_outcome = models[f'outcome_{model_key}'].predict_proba(input_array)
        prediction_hospitalstay = models[f'hospitalstay_{model_key}'].predict(input_array)
        probabilities_hospitalstay = models[f'hospitalstay_{model_key}'].predict_proba(input_array)
    
    # 介護申請の必要性予測
    input_array_2 = input_data = np.delete(input_array, [13, 14, 15], axis=1)
    if input_array[0][16] == 0:  # 予定外_1
        prediction_nursingcare = models['nursingcare_p'].predict(input_array_2)
        probabilities_nursingcare = models['nursingcare_p'].predict_proba(input_array_2)
    else:
        prediction_nursingcare = models['nursingcare_e'].predict(input_array_2)
        probabilities_nursingcare = models['nursingcare_e'].predict_proba(input_array_2)

    return {
        "予想される退院経路": {
            "死亡の確率": f"{probabilities_outcome[0][0] * 100:.1f}%",
            "転院の確率": f"{probabilities_outcome[0][1] * 100:.1f}%"
        },
        "予想される入院期間": {
            "1週間以内の確率": f"{probabilities_hospitalstay[0][0] * 100:.1f}%",
            "1-2週間の確率": f"{probabilities_hospitalstay[0][1] * 100:.1f}%",
            "2-3週間の確率": f"{probabilities_hospitalstay[0][2] * 100:.1f}%",
            "3週間以上の確率": f"{probabilities_hospitalstay[0][3] * 100:.1f}%"
        },
        "介護申請の必要性(判定1)": {
            "判定": (
                "必要です" if (probabilities_outcome[0][1] * 100 >= 20 or probabilities_hospitalstay[0][3] * 100 >= 20) and input_array[0][14] == 1 and input_array[0][1] >= 4
                else "申請中です(地域包括支援センターに有事相談できます)" if input_array[0][14] == 1 and input_array[0][13] == 0 and input_array[0][15] == 0
                else "まだしなくて良い" if input_array[0][14] == 1
                else "取得済みです(地域包括支援センターに有事相談できます)"
            )
        },
        "介護申請の必要性(判定2)": {
            "介護申請が必要な確率": f"{probabilities_nursingcare[0][1] * 100:.1f}%",
            "判定": (
                "必要です" if probabilities_nursingcare[0][1] * 100 >= 30 and input_array[0][1] >= 4 and input_array[0][14] == 1
                else "申請中です(地域包括支援センターに有事相談できます)" if input_array[0][14] == 1 and input_array[0][13] == 0 and input_array[0][15] == 0
                else "まだしなくて良い" if input_array[0][14] == 1
                else "取得済みです(地域包括支援センターに有事相談できます)"
            )
        }
    }
