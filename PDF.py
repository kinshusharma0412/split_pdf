import os
from fpdf import FPDF
import streamlit as st
from PIL import Image
import glob
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
		
		image_list.append(name)
		st.write(image1.size)
		
		dict.append(image1)
		if image_size_x<image1.size[0]:
			image_size_x=image1.size[0]
		image_size_y.append(image1.size[1])
		
	pdf=FPDF()
	pdf.add_page()
	for y in range(len(image_list)):
		st.write(image_size_x,image_size_y[y])
		pdf.image(image_list[y])
		st.write(pdf)
	pdf.output("@Polls_Quiz.pdf", "F")
	with open("./@Polls_Quiz.pdf", "rb") as file:
		btn = st.download_button(label="Download image",data=file,file_name="@Polls_Quiz.pdf",mime="application/octet-stream")
		
