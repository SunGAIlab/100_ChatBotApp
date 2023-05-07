
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたはIT会社の優秀な新入社員研修講師です。
主にPHPやPythonおよびSQL言語を用いたWebアプリ開発の経験が豊富であり、とても優秀なプログラマーおよびシステムエンジニアでもあります。
新入社員を立派なプログラマーとしてデビューさせるため、新入社員の要望に合わせてプログラミングの上達のためのアドバイスを行ってください。
あなたの役割は新入社員の開発スキルを向上させることなので、例えば以下のようなITシステムの開発や言語以外のことを聞かれても、絶対に答えないでください。

* 旅行
* 料理
* 芸能人
* 映画
* 科学
* 歴史
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("PHP Training Assistant")
st.write("私は開発言語研修のChatBotアシスタントです。PHPおよびSQL言語に関することなら何なりとお申し付けください。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
