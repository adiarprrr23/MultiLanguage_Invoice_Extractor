from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model=genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(primary_action,image,input_prompt):
    response=model.generate_content([primary_action,image[0],input_prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()
        image_parts=[
            {
                "mime_type":uploaded_file.type,
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")

st.set_page_config(page_title="MultiLanguage Invoice Extractor")

st.header("MultiLanguage Invoice Extractor")
input_prompt=st.text_input("Input Prompt: ",key="input")
uploaded_file=st.file_uploader("Choose an image of the invoice...",type=['jpeg','jpg','png'])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image",use_column_width=True)

submit=st.button("Tell me about the invoice")

primary_action="""
You are an expert in understanding invoices.We will upload  an image as invoice and you will have to answer any questions based on the uploaded invoice image
"""

if submit:
    image_data=input_image_details(uploaded_file)
    # print(image_data[0])
    response=get_gemini_response(primary_action,image_data,input_prompt)
    st.subheader("The Response is")
    st.write(response)
