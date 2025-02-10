python model.py
uvicorn main:app --reload
streamlit run ui.py

# フォントを変える
st.markdown("<h1 style='font-size:24px; color:blue;'>推論結果</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='font-size:20px; color:blue;'>推論結果</h2>", unsafe_allow_html=True)
# 1マスずらす
st.markdown("<div style='margin-left: 20px;'>このテキストは右にずれています。</div>", unsafe_allow_html=True)
