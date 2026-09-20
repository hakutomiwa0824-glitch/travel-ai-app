import streamlit as st
from openai import OpenAI

# ページタイトル設定
st.title("✈️ AIトラベルコンシェルジュ")
st.write("あなたの希望に合った旅行プランを提案します！")

# OpenAI APIキーの設定（サイドバーで入力）
api_key = st.sidebar.text_input("OpenAI API Key", type="password")

if not api_key:
    st.info("左側のサイドバーにOpenAIのAPIキーを入力してください。")
    st.stop()

# クライアントの初期化
client = OpenAI(api_key=api_key)

# システムプロンプト（旅行AIとしての基本役割）
SYSTEM_PROMPT = """
あなたはプロの旅行プランナー「TravelBot」です。
ユーザーの希望に合わせて、現実的で魅力的、かつ効率的な旅行プランを提案してください。

以下の条件を確認しつつ、タイムスケジュール付きのプランを作成してください。
1. 行き先・雰囲気
2. 日程・日数
3. 予算感
4. 同行者
5. 移動手段
"""

# セッション状態の初期化（会話履歴を保持）
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "こんにちは！どんな旅行に行きたいですか？（例：来月の週末に、東京発で温泉に行きたいです！）"}
    ]

# 過去の会話を表示（systemメッセージ以外）
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# ユーザーからの入力処理
if prompt := st.chat_input("旅行の希望を入力してください..."):
    # ユーザーのメッセージを追加・表示
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # AIの回答を取得・表示
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages
        )
        ai_message = response.choices[0].message.content
        st.write(ai_message)

    # AIのメッセージを履歴に追加
    st.session_state.messages.append({"role": "assistant", "content": ai_message})