import os
from fpdf import FPDF
import streamlit as st
from PIL import Image
import glob,img2pdf
#from PyPDF2 import PdfReader, PdfWriter, PageObject
from random import randint

on = st.empty()
pdf_path="./@Polls_Quiz.pdf"

if 'img' not in st.session_state:
	st.session_state.img = []
if 'clicked' not in st.session_state:
	st.session_state.clicked = True
if 'dow' not in st.session_state:
	st.session_state.dow = False
if on.toggle('Image to PDF feature'):
	st.write('Activate Image to PDF feature')
	place_holder=st.empty()
	with place_holder.form(key="form"):
		multiple = st.empty()
		multiple.toggle('Do you want to same image comes multiple times in pdf if you upload it multiple times')
		uploaded_files = st.file_uploader("Choose a image file (multiple files are accepted)", accept_multiple_files=True)
		submit_button = st.empty()
	if submit_button.form_submit_button(label="Submit your choice"):
		for uploaded_file in uploaded_files:
				if multiple:
					st.write("1")
					name="./"+uploaded_file.name
					with open(name, "wb") as file:
						file.write(uploaded_file.getvalue())
					st.session_state["img"].append((name))
				else:
					st.write("2")
					name="./"+uploaded_file.name
					if name not in st.session_state["img"]:
						with open(name, "wb") as file:
							file.write(uploaded_file.getvalue())
						st.session_state["img"].append((name))
		file = open(pdf_path, "wb")
		file.write(img2pdf.convert(st.session_state["img"]))
		file.close()
		with open(pdf_path, "rb") as file:
			if st.download_button(label="Download PDF",data=file,file_name="@Polls_Quiz.pdf",mime="application/octet-stream"):
				on.empty()
				#on.toggle('Image to PDF feature')
				place_holder.empty()
		
					
		