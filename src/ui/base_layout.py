import streamlit as st
def style_backgroud_home():
  st.markdown("""
    <style>
              .stApp{
                background: #5865F2 !important;
              }

              .stApp div[data-testid="stColumn"]{
                background: #E0E3FF !important;
                padding:2.5rem !important;
                border-radius: 5rem !important;
              }
              
    </style>
  """,unsafe_allow_html=True)


def style_backgroud_dashboard():
  st.markdown("""
    <style>
              .stApp{
                background: #5865F2 !important;
              }
              
    </style>
  """,unsafe_allow_html=True)


def style_base_layout():
  st.markdown("""
    <style>
              @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
              @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&family=Outfit:wght@100..900&display=swap');

            
              /* Hide Top Bar of streamlit */
              #MainMenu, footer, header {
                visibility: hidden;
              }

              .block-container {
                padding-top:1.5rem !important;
              }

              h1{
              font-family: 'Climate Crisis', sans-serif;
              font-size: 3.5rem !important;
              line-height: 0.9 !important;
              margin-bottom: 0rem !important;
              }

              h2{
              font-family: 'Climate Crisis', sans-serif;
              font-size: 2rem !important;
              line-height: !important;
              margin-bottom: 0rem !important;
              }
              
              h3,h4,p{
              font-family: 'Outfit', sans-serif;
              }

              button{
              background: #5865F2 !important;
              border-radius: 1.5rem !important;
              color: #fff !important;
              padding: 10px 20px !important;
              border: none !important;
              transition: transform 0.25s ease-in-out !important;
              }

              button[kind="secondary"]{
              background: #E8459E !important;
              border-radius: 1.5rem !important;
              color: #fff !important;
              padding: 10px 20px !important;
              border: none !important;
              transition: transform 0.25s ease-in-out !important;
              }

              button[kind="tertiary"]{
              background: #black !important;
              border-radius: 1.5rem !important;
              color: #fff !important;
              padding: 10px 20px !important;
              border: none !important;
              transition: transform 0.25s ease-in-out !important;
              }

              button:hover{
              transform: scale(1.05) !important;
              }
    </style>
  """,unsafe_allow_html=True)