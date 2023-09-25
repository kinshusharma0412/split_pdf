import os
from fpdf import FPDF
import streamlit as st
from PIL import Image
import glob,img2pdf
#from PyPDF2 import PdfReader, PdfWriter, PageObject
on = st.toggle('Image to PDF feature')
pdf_path="./@Polls_Quiz.pdf"

if 'img' not in st.session_state:
	st.session_state.img = []
if 'clicked' not in st.session_state:
	st.session_state.clicked = True
if 'dow' not in st.session_state:
	st.session_state.dow = False
if on:
	st.write('Activate Image to PDF feature')
	uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
	pq=st.empty()
	
	if uploaded_files:
		if len(st.session_state["img"])!=0:
			file = open(pdf_path, "wb")
			file.write(img2pdf.convert(st.session_state["img"]))
			file.close()
			with open(pdf_path, "rb") as file:
				if pq.download_button(label="Download PDF",data=file,file_name="@Polls_Quiz.pdf",mime="application/octet-stream"):l
					st.stop()
		if st.session_state.clicked:
			dict=[]
			for uploaded_file in uploaded_files:
				name="./"+uploaded_file.name
				with open(name, "wb") as file:
					file.write(uploaded_file.getvalue())
				st.session_state["img"].append((name))
		if st.session_state.clicked:
			st.session_state.clicked = False
			file = open(pdf_path, "wb")
			file.write(img2pdf.convert(st.session_state["img"]))
			file.close()
			with open(pdf_path, "rb") as file:
				if pq.download_button(label="Download PDF",data=file,file_name="@Polls_Quiz.pdf",mime="application/octet-stream"):
		else:
			st.session_state.clicked=True
		
	
		
		

			
		
	
		
	
		
	
		
