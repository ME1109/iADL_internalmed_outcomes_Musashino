import streamlit as st
import numpy as np
import pandas as pd
from model import models
from main import make_predictions  # 修正: main.py の関数を使用

# ページレイアウトをワイドに設定
st.set_page_config(layout="wide")

# ヘッダーとメインコンテンツの余白を減らすCSS
st.markdown(
    """
    <style>
        /* ヘッダーの余白を削減 */
        .css-18e3th9 {
            padding-top: 0rem;
            padding-bottom: 0rem;
        }
        /* メインコンテンツの余白を削減 */
        .main .block-container {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# タイトル
st.markdown("<h1 style='font-size:24px; color:blue;'>自宅での日常生活動作(ADL)で内科入院の期間や転帰を予測する：</h1>", unsafe_allow_html=True)

# ★★各種ウィジェット定義★★
# 7列にして表示する
col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 0.1, 1, 0.1, 1, 0.1, 1])
with col1:
    # 性別
    sex = st.radio('性別:', ['男', '女'])
    sex_value = 1 if sex == '男' else 0
    # 年齢10群
    age = st.slider('年齢:', 0, 110, 25)
    def age_group(age):
        if 0 <= age <= 50:
            return 0
        elif 51 <= age <= 55:
            return 1
        elif 56 <= age <= 60:
            return 2
        elif 61 <= age <= 65:
            return 3
        elif 66 <= age <= 70:
            return 4
        elif 71 <= age <= 75:
            return 5
        elif 76 <= age <= 80:
            return 6
        elif 81 <= age <= 85:
            return 7
        elif 86 <= age <= 90:
            return 8
        elif 91 <= age <= 110:
            return 9
        else:
            return None
    age_group_value = age_group(age)
    # 介護認定
    care = st.radio('介護認定:', ['要介護・要支援を取得済', '申請中', '未申請'])
    介護_取得済 = 0
    介護_未取得 = 0
    介護_対象外 = 0
    if care == '要介護・要支援を取得済':
        介護_取得済 = 1
    elif care == '申請中':
        介護_未取得 = 1
    elif care == '未申請':
        if age < 65:
            介護_対象外 = 1
        else:
            介護_未取得 = 1
    # 診療科
    department = st.radio('診療科:', ['救命科', '消化器内科', '循環器内科', '呼吸器内科', '脳神経内科', '血液内科', 'その他'])
    department_values = {'救命科': 0, '消化器内科': 0, '循環器内科': 0, '呼吸器内科': 0, '脳神経内科': 0, '血液内科': 0, 'その他': 0}
    department_values[department] = 1
    # 入院経路の選択肢を作成
    admission_route = st.radio('入院経路:', ['予定入院', '予定外・緊急の入院'])
    admission_route_value = 0 if admission_route == '予定入院' else 1

with col2:
    st.markdown("<div style='border-left: 10px solid balck; height: 100%;'></div>", unsafe_allow_html=True)

with col3:
    # 食事
    meal = st.radio('食事:', ['全介助', '一部介助', '自立'])
    meal_value = {'全介助': 0, '一部介助': 1, '自立': 2}[meal]
    # 移乗
    transfer = st.radio('移乗:', ['全介助', '一部介助', '見守り', '自立'])
    transfer_value = {'全介助': 0, '一部介助': 1, '見守り': 2, '自立': 3}[transfer]
    # 整容
    hairdressing = st.radio('整容:', ['介助', '自立'])
    hairdressing_value = {'介助': 0, '自立': 1}[hairdressing]
    # トイレ動作
    toilet = st.radio('トイレ動作:', ['全介助', '一部介助', '自立'])
    toilet_value = {'全介助': 0, '一部介助': 1, '自立': 2}[toilet]
    # 排便管理
    poop = st.radio('排便管理:', ['全介助', '一部介助', '自立'])
    poop_value = {'全介助': 0, '一部介助': 1, '自立': 2}[poop]
    # 排尿管理
    urination = st.radio('排尿管理:', ['全介助', '一部介助', '自立'])
    urination_value = {'全介助': 0, '一部介助': 1, '自立': 2}[urination]

with col4:
    st.markdown("<div style='border-left: 10px solid black; height: 100%;'></div>", unsafe_allow_html=True)

with col5:
    # 平地歩行
    walking = st.radio('平地歩行:', ['歩行困難', '一部介助', '見守り', '自立'])
    walking_value = {'歩行困難': 0, '一部介助': 1, '見守り': 2, '自立': 3}[walking]
    # 階段
    stairs = st.radio('階段:', ['困難', '一部介助', '自立'])
    stairs_value = {'困難': 0, '一部介助': 1, '自立': 2}[stairs]
    # 更衣
    wearing = st.radio('更衣:', ['全介助', '一部介助', '自立'])
    wearing_value = {'全介助': 0, '一部介助': 1, '自立': 2}[wearing]
    # 入浴
    bathing = st.radio('入浴:', ['介助', '自立'])
    bathing_value = {'介助': 0, '自立': 1}[bathing]
    # 認知症自立度
    dementia = st.radio('認知症自立度:', ['自立', '見守り～要介護'])
    dementia_value = {'自立': 0, '見守り～要介護': 1}[dementia]

with col6:
    st.markdown("<div style='border-left: 10px solid black; height: 100%;'></div>", unsafe_allow_html=True)

with col7:
    # 推論を実行するボタン
    if st.button('推論を実行'):
        input_data = {
            '男_1': sex_value,
            '年齢群': age_group_value,
            '食事': meal_value,
            '移乗': transfer_value,
            '整容': hairdressing_value,
            'トイレ動作': toilet_value,
            '入浴': bathing_value,
            '平地歩行': walking_value,
            '階段': stairs_value,
            '更衣': wearing_value,
            '排便管理': poop_value,
            '排尿管理': urination_value,
            '認知症自立度': dementia_value,
            '介護_取得済': 介護_取得済,
            '介護_未取得': 介護_未取得,
            '介護_対象外': 介護_対象外,
            '予定外_1': admission_route_value,
            '診療科_救命科': department_values['救命科'],
            '診療科_消化器内科': department_values['消化器内科'],
            '診療科_循環器内科': department_values['循環器内科'],
            '診療科_呼吸器内科': department_values['呼吸器内科'],
            '診療科_脳神経内科': department_values['脳神経内科'],
            '診療科_血液内科': department_values['血液内科'],
            '診療科_その他': department_values['その他']
        }
        input_df = pd.DataFrame([input_data])
        input_array = input_df.values
        result = make_predictions(input_array)

        # 結果を表示
        st.markdown("<h1 style='font-size:24px; color:black;'>推論結果：</h1>", unsafe_allow_html=True)
        st.markdown("<h1 style='font-size:24px; color:blue;'>予想される退院経路:</h1>", unsafe_allow_html=True)
#        st.write(f'死亡の確率: {probabilities_outcome[0][0] * 100:.1f}%')
#        st.write(f'転院の確率: {probabilities_outcome[0][1] * 100:.1f}%')
        st.write(f'死亡の確率: {result["予想される退院経路"]["死亡の確率"]}')
        st.write(f'転院の確率: {result["予想される退院経路"]["転院の確率"]}')
        
        st.markdown("<h1 style='font-size:24px; color:blue;'>予想される入院期間：</h1>", unsafe_allow_html=True)
        st.write(f'  1週間以内の確率: {result["予想される入院期間"]["1週間以内の確率"]}')
        stay_prob_1_2 = float(result["予想される入院期間"]["1-2週間の確率"].replace('%', ''))
        stay_prob_2_3 = float(result["予想される入院期間"]["2-3週間の確率"].replace('%', ''))
        st.write(f'  1-3週間の確率: {stay_prob_1_2 + stay_prob_2_3:.1f}%')
        st.write(f'  3週間以上の確率: {result["予想される入院期間"]["3週間以上の確率"]}')
#        st.write(f'  1週間以内の確率: {probabilities_hospitalstay[0][0] * 100:.1f}%')
#        stay_prob_1_2 = float(probabilities_hospitalstay[0][1] * 100)
#        stay_prob_2_3 = float(probabilities_hospitalstay[0][2] * 100)
#        st.write(f'  1-3週間の確率: {stay_prob_1_2 + stay_prob_2_3:.1f}%')
#        st.write(f'  3週間以上の確率: {probabilities_hospitalstay[0][3] * 100:.1f}%')

        st.markdown("<h1 style='font-size:24px; color:blue;'>介護申請の必要性(判定1)：</h1>", unsafe_allow_html=True)
        transfer_prob = float(result["予想される退院経路"]["転院の確率"].replace('%', ''))
        stay_prob_3_plus = float(result["予想される入院期間"]["3週間以上の確率"].replace('%', ''))
#        transfer_prob = float(probabilities_outcome[0][1] * 100)
#        stay_prob_3_plus = float(probabilities_hospitalstay[0][3] * 100)
        care_status_1 = care
        care_needs_1 = 'まだしなくて良い'  # デフォルトを設定
        if care_status_1 == '要介護・要支援を取得済':
            care_needs_1 = '取得済みです(地域包括支援センターに有事相談できます)'
        elif care_status_1 == '申請中':
            care_needs_1 = '申請中です(地域包括支援センターに有事相談できます)'

        if (transfer_prob >= 20) or (stay_prob_3_plus >= 20):
            if (care_status_1 == '未申請') and (age >= 65):
                care_needs_1 = '必要です'

        st.write(f'転院率・3週超の入院率(≥20%)で判定')
        st.markdown(f"<span style='color:red; font-weight:bold;'> 申請は、{care_needs_1}</span>", unsafe_allow_html=True)
        
        st.markdown("<h1 style='font-size:24px; color:blue;'>介護申請の必要性(判定2)：</h1>", unsafe_allow_html=True)
        st.write(f'転院率・3週超えの入院率の予測モデル')
        care_status_2 = care
        care_needs_2 = 'まだしなくて良いです'  # デフォルトを設定
        if care_status_2 == '要介護・要支援を取得済':
            care_needs_2 = '取得済みです(地域包括支援センターに有事相談できます)'
        elif care_status_2 == '申請中':
            care_needs_2 = '申請中です(地域包括支援センターに有事相談できます)'
        nursing_care_prob = float(result["介護申請の必要性(判定2)"]["介護申請が必要な確率"].replace('%', ''))
#        nursing_care_prob = float(probabilities_nursingcare[0][1] * 100)
        if nursing_care_prob >= 30:
            if (care_status_1 == '未申請') and (age >= 65):
                care_needs_2 = '必要です'
        st.write(f'  介護申請が必要な確率: {result["介護申請の必要性(判定2)"]["介護申請が必要な確率"]}')
#        st.write(f'  介護申請が必要な確率: {nursing_care_prob:.1f}%')
        st.markdown(f"<span style='color:red; font-weight:bold;'> 申請は、{care_needs_2}</span>", unsafe_allow_html=True)
