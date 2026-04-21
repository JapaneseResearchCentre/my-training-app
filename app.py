import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# --- ログイン機能の追加 ---
def check_password():
    """パスワードが正しいか確認する関数"""
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # セッションから削除して安全に
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # 初回表示
        st.text_input("パスワードを入力してください", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # パスワードが間違っている場合
        st.text_input("パスワードが違います。再度入力してください", type="password", on_change=password_entered, key="password")
        st.error("😕 パスワードが正しくありません")
        return False
    else:
        # パスワード正解
        return True

if not check_password():
    st.stop()  # パスワードが正しくなければ、これ以降のコードを実行しない

# --- ここから下に今までのプログラムを書く ---
DB_FILE = 'training_data.db'

# (以下、以前作成した init_db, add_data などのコードをそのまま続ける)
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS logs (date TEXT, weight REAL, menu TEXT)')

def add_data(weight, menu):
    with sqlite3.connect(DB_FILE) as conn:
        date = datetime.now().strftime('%Y-%m-%d %H:%M')
        conn.execute('INSERT INTO logs VALUES (?, ?, ?)', (date, weight, menu))

st.title("💪 Yuichi's Private Log")
init_db()

with st.form("input_form", clear_on_submit=True):
    weight = st.number_input("体重 (kg)", min_value=0.0, value=70.0, step=0.1)
    menu = st.text_area("メニュー内容")
    if st.form_submit_button("保存する"):
        add_data(weight, menu)
        st.success("保存完了！")

st.divider()

try:
    with sqlite3.connect(DB_FILE) as conn:
        df = pd.read_sql_query("SELECT * FROM logs ORDER BY date DESC", conn)
    if not df.empty:
        st.table(df)
except:
    pass