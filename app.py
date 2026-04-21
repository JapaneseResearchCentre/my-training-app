import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# データベース設定
DB_FILE = 'training_log.db'

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS logs (date TEXT, weight REAL, menu TEXT)')

def add_data(weight, menu):
    with sqlite3.connect(DB_FILE) as conn:
        date = datetime.now().strftime('%Y-%m-%d')
        conn.execute('INSERT INTO logs VALUES (?, ?, ?)', (date, weight, menu))

# UI部分
st.title("💪 筋トレ記録アプリ")

# 入力フォーム
with st.form("input_form"):
    weight = st.number_input("体重 (kg)", min_value=0.0, format="%.1f")
    menu = st.text_area("今日のメニュー")
    submitted = st.form_submit_button("記録する")
    
    if submitted:
        init_db()
        add_data(weight, menu)
        st.success("記録しました！")

# 履歴表示
st.subheader("📊 トレーニング履歴")
init_db()
with sqlite3.connect(DB_FILE) as conn:
    df = pd.read_sql_query("SELECT * FROM logs ORDER BY date DESC", conn)
    st.table(df)