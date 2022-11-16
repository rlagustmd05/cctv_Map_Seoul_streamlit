import folium
import streamlit as st
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import sqlite3
import pandas as pd
import json

con = sqlite3.connect('db.db')
cur = con.cursor()

def login_user(id, pwd):
    cur.execute(f"SELECT * FROM users WHERE id='{id}' and pw='{pwd}'")
    return cur.fetchone()

menu = st.sidebar.selectbox('MENU', options=['회원가입','로그인','회원목록','강남 지키미'])

if menu == '회원가입':
    with st.form('my_form', clear_on_submit=True):
        id = st.text_input('아이디', placeholder='아이디를 입력하세요.', max_chars=10)
        pw = st.text_input('비밀번호', placeholder='비밀번호를 입력하세요.', type='password')
        pw_ck = st.text_input('비밀번호 확인', placeholder='비밀번호를 확인하세요.', type='password')
        name = st.text_input('이름', placeholder='ex) 방민예')
        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.text_input('나이', placeholder='ex) 18')
        with col2:
            gender = st.radio('성별', ['남자', '여자'], horizontal=True)
        number = st.text_input('전화번호', placeholder='ex) 010-8071-9071')
        register = st.form_submit_button('회원가입')

        if register:
            if pw == pw_ck:
                cur.execute(f"INSERT INTO users(id, pw, name, age, gender, number) "
                            f"VALUES("
                            f"'{id}', '{pw}', '{name}', {age}, '{gender}', '{number}')")
                con.commit()
                st.success('회원가입이 완료되었습니다.')
            else:
                st.warning('비밀번호를 확인해주세요.')

if menu =='로그인':
    login_id = st.sidebar.text_input('아이디')
    login_pw = st.sidebar.text_input('비밀번호', type='password')
    login_btn = st.sidebar.button('로그인')
    if login_btn:
        user_info = login_user(login_id, login_pw)
        if user_info:
            st.subheader(user_info[2]+'님 환영합니다.')
            st.image(user_info[0]+'.jpg',width=500)
        else:
            st.subheader('다시 로그인하세요')

if menu == '회원목록':
    st.subheader('회원목록')
    df = pd.read_sql("SELECT name, age, gender FROM users", con)
    st.dataframe(df, 500,280)

if menu == '강남 지키미':
    df = pd.read_csv('Project.csv',encoding='cp949')
    df_area = df[df['자치구'] == '강남구']
    df_area = df[['위도','경도']]

    st.title('강남 지키미!')

    m = folium.Map(location=[37.494422408892, 127.06315179125], zoom_start=13)

    marker_cluster = MarkerCluster().add_to(m)

    for lat, long in zip(df_area['위도'], df_area['경도']):
        folium.Marker([lat, long],
                      popup="방범용",
                      tooltip="방범용",
                      icon=folium.Icon(icon = 'facetime-video', color = 'red')).add_to(marker_cluster)

    with open("boundary.txt", "r",encoding='UTF-8') as file:
        data = file.read()
    seoul_geo = json.loads(data)

    folium.GeoJson(
        seoul_geo,
        name="강남구"
    ).add_to(m)

    st_data = st_folium(m, width = 725)