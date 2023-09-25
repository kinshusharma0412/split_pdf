import os
from fpdf import FPDF
import streamlit as st
from PIL import Image
import glob,img2pdf
#from PyPDF2 import PdfReader, PdfWriter, PageObject
on = st.toggle('Image to PDF feature')

if on:
	st.write('Activate Image to PDF feature')
	uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
	dict=[]
	image_size_x=0
	image_size_y=[]
	image_list=[]
	
	
	for uploaded_file in uploaded_files:
		name="./"+uploaded_file.name
		st.write(uploaded_file)
		
		with open(name, "wb") as file:
			file.write(uploaded_file.getvalue())
		image1 = Image.open(name)
		
		image_list.append(img2pdf.convert(image1.filename))
		
		
	pdf_path="./@Polls_Quiz.pdf"
	file = open(pdf_path, "wb")
	for y in image_list:
		file.write(y)
	file.close()
		
	with open(pdf_path, "rb") as file:
		btn = st.download_button(label="Download PDF",data=file,file_name="@Polls_Quiz.pdf",mime="application/octet-stream")
		
