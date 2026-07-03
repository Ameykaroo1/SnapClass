import streamlit as st

def header_home():
  logo_url = "https://i.ibb.co/0j1Z3kM/Snap-Class-Logo.png"
  st.markdown(f"""
              <div style="display: flex; 
              flex-direction: column; align-items: center; justify-content: center; margin-bottom: 30px; margin-top: 30px;">
                <img src='{logo_url}' style='height:100px;'/>
                <h1 style='text-align:center; color:#e0e3FF;'>Snap <br/>Class</h1>
              </div>
""",unsafe_allow_html=True)
