import os,time
from fpdf import FPDF
import streamlit as st
from PIL import Image
import glob,img2pdf
from PyPDF2 import PdfWriter, PdfReader,PdfMerger, PdfReader
from random import randint
import tabula
import pdfkit
import pandas as pd
import sys
from PDFNetPython3.PDFNetPython import PDFDoc, Optimizer, SDFDoc, PDFNet
on = st.empty()
bttn=st.empty()
onn= st.empty()
onn1= st.empty()

onon= st.empty()
pdf_path="./@Polls_Quiz.pdf"

def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"
def compress_file(input_file: str, output_file: str):
    """Compress PDF file"""
    if not output_file:
        output_file = input_file
    initial_size = os.path.getsize(input_file)
    try:
        # Initialize the library
        PDFNet.Initialize()
        doc = PDFDoc(input_file)
        # Optimize PDF with the default settings
        doc.InitSecurityHandler()
        # Reduce PDF size by removing redundant information and compressing data streams
        Optimizer.Optimize(doc)
        doc.Save(output_file, SDFDoc.e_linearized)
        doc.Close()
    except Exception as e:
        print("Error compress_file=", e)
        doc.Close()
        return False
    compressed_size = os.path.getsize(output_file)
    ratio = 1 - (compressed_size / initial_size)
    summary = {
        "Input File": input_file, "Initial Size": get_size_format(initial_size),
        "Output File": output_file, f"Compressed Size": get_size_format(compressed_size),
        "Compression Ratio": "{0:.3%}.".format(ratio)
    }
    # Printing Summary
    
    st.write("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
    return True

if 'img' not in st.session_state:
	st.session_state.img = []
if 'clicked' not in st.session_state:
	st.session_state.clicked = True
if 'dow' not in st.session_state:
	st.session_state.dow = False


	
if on.toggle('Image to PDF feature'):
	st.write('Activate Image to PDF feature')
	tm=st.empty()
	place_holder=st.empty()
	st.session_state.back = False
	opaque=0
	new_list_name=[]
	with place_holder.form(key="form1"):
		if tm.toggle('Add Background image to PDF'):
			back_uploaded_files = st.file_uploader("Choose a background image file (remember i will convert your image to square image)", accept_multiple_files=False)
			line=st.empty()
			opaque = line.slider('Select background image opacity', 0, 255, 100)
			if back_uploaded_files:
				st.session_state.back = True
			
		multiple=st.toggle('Do you want to same image comes multiple times in pdf if you upload it multiple times')
		uploaded_files = st.file_uploader("Choose a image file (multiple files are accepted)", accept_multiple_files=True)
		submit_button = st.empty()
		
	if submit_button.form_submit_button(label="Submit your choice"):
		 
		if st.session_state.back:
			back_name="./"+back_uploaded_files.name+".png"
			with open(back_name, "wb") as file:
				file.write(back_uploaded_files.getvalue())
			
			
			
		for uploaded_file in uploaded_files:
				if multiple:
					
					name="./"+uploaded_file.name+".png"
					with open(name, "wb") as file:
						file.write(uploaded_file.getvalue())
					st.session_state["img"].append((name))
				else:
					
					name="./"+uploaded_file.name
					if name not in st.session_state["img"]:
						with open(name, "wb") as file:
							file.write(uploaded_file.getvalue())
						
						st.session_state["img"].append((name))
		xxx=0
		for x in st.session_state["img"]:
			im = Image.open(x).size[0]
			xxx=im+xxx
		xxx=xxx//len(st.session_state["img"])
		if st.session_state.back:
			for x in st.session_state["img"]:
				im = Image.open(x)
				formet=im.format
				opaque=opaque
				back_ground= Image.open(back_name)
				new=im.resize((xxx, im.size[1]))
				new.save(x)
				formet="PNG"
				
				if xxx>im.size[1]:
					back_resize=back_ground.resize((im.size[1],im.size[1]))
					
					back_resize.save(back_name)
					back_ground= Image.open(back_name)
					back_ground = back_ground.convert('RGBA')
					newImage = []
					for item in back_ground.getdata():
						if ( item[0] >230 and item[1] >230 and item[2] >230 ) or ( item[0] <35 and item[1] <35 and item[2] <35 ):
							newImage.append((255, 255, 255, 0))
						else:
							newImage.append((item[0],item[1],item[2],opaque))
					back_ground.putdata(newImage)
					back_ground.save('output.png')
					im = Image.open(x)
					back_ground= Image.open("output.png")
					myMerged_image = Image.new("RGBA", im.size)
					myMerged_image.paste(im, (0,0))
					_, _, _, mask = back_ground.split()
					myMerged_image.paste(back_ground, ((xxx-im.size[1])//2,0), mask)
					myMerged_image.save(x+".png",formet)
				else:
					back_resize=back_ground.resize((xxx,xxx))
					back_resize.save(back_name)
					
					back_ground= Image.open(back_name)
					
					back_ground = back_ground.convert('RGBA')
					newImage = []
					for item in back_ground.getdata():
						if ( item[0] >230 and item[1] >230 and item[2] >230 ) or ( item[0] <35 and item[1] <35 and item[2] <35 ):
							newImage.append((255, 255, 255, 0))
							
						else:
							newImage.append((item[0],item[1],item[2], opaque))
					back_ground.putdata(newImage)
					back_ground.save('output.png')
					im = Image.open(x)
					back_ground= Image.open("output.png")
					
					myMerged_image = Image.new("RGBA", im.size)
					myMerged_image.paste(im, (0,0))
					_, _, _, mask = back_ground.split()
					myMerged_image.paste(back_ground, (0, (im.size[1]-xxx)//2), mask)
					myMerged_image.save(x+".png",formet)
				if x+".png" not in new_list_name:
					new_list_name.append(x+".png")
				st.image(x+".png")
				
				

		else:
			
			for x in st.session_state["img"]:
				im = Image.open(x)
				new=im.resize((xxx, im.size[1]))
				new.save(x)
		file = open(pdf_path, "wb")
		if len(new_list_name)==0:
			file.write(img2pdf.convert(st.session_state["img"]))
		else:
			file.write(img2pdf.convert(new_list_name))
		file.close()
		with open(pdf_path, "rb") as file:
			if st.download_button(label="Download PDF",data=file,file_name="@Polls_Quiz.pdf",mime="application/octet-stream"):
				on.empty()
				#on.toggle('Image to PDF feature')
				place_holder.empty()
elif onon.toggle('PDF Spliter feature'):
	st.write("This feature can split your PDF into multiple PDF")
	place_holder=st.empty()
	with place_holder.form(key="form2"):
		uploaded_files = st.file_uploader("Choose a PDF file (multiple files are not accepted)", accept_multiple_files=False)
		line=st.empty()
		submit_button = st.empty()
		if uploaded_files:
			name="./"+uploaded_files.name
			with open(name, "wb") as file:
				file.write(uploaded_files.getvalue())
			inputpdf = PdfReader(open(name, "rb"))
			
			pagen = line.slider('Select page number', 0, len(inputpdf.pages), 0)
	if submit_button.form_submit_button(label="Submit your choice"):
		if pagen>0:
			for i in range((len(inputpdf.pages)//pagen)):
				output = PdfWriter()
				for x in range((pagen)):
					output.add_page(inputpdf.pages[x*i])
				with open(name[2:-4]+" %s.pdf" % (i+1), "wb") as outputStream:
					output.write(outputStream)
				file = open(name[2:-4]+" %s.pdf" % (i+1),"rb")
				st.download_button(label="Download PDF",data=file.read(),file_name=name[2:-4]+" %s.pdf" % (i+1),mime="application/octet-stream")
			output = PdfWriter()
			if (len(inputpdf.pages)//pagen)*pagen!=len(inputpdf.pages):
				for i in range((len(inputpdf.pages)//pagen)*pagen,len(inputpdf.pages)):
					output.add_page(inputpdf.pages[i])
				with open(name[2:-4]+" %s.pdf" % ((len(inputpdf.pages)//pagen)+1), "wb") as outputStream:
					output.write(outputStream)
				file = open(name[2:-4]+" %s.pdf" % ((len(inputpdf.pages)//pagen)+1),"rb")
				st.download_button(label="Download PDF",data=file.read(),file_name=name[2:-4]+" %s.pdf" %str(len(inputpdf.pages)//pagen+1),mime="application/octet-stream")

elif onn.toggle('Excle to PDF feature'):
# Read pdf into a list of DataFrame
	st.write("This feature can convert your Excel file into PDF file")
	place_holder=st.empty()
	with place_holder.form(key="form2"):
		uploaded_files = st.file_uploader("Choose a .xlsx file (multiple files are not accepted)", accept_multiple_files=False)
		line=st.empty()
		submit_button = st.empty()
		if uploaded_files:
			name="./"+uploaded_files.name
			with open(name, "wb") as file:
				file.write(uploaded_files.getvalue())
			
	if submit_button.form_submit_button(label="Submit your choice"):
		name="./"+uploaded_files.name
		sheet_names = pd.ExcelFile(name)
		dff=[]
		y=0
		
		for x in sheet_names.sheet_names:
			df = pd.read_excel(name,x)
			df.to_html(name[:-5]+".html")
			pdfkit.from_file(name[:-5]+".html", name[:-5]+x+".pdf")
			dff.append(name[:-5]+x+".pdf")
		merger = PdfMerger()
		for filename in dff:
			pdfFile = open(filename, 'rb')
			pdfReader = PdfReader(pdfFile)
			merger.append(pdfReader)
		merger.write(name[:-5]+".pdf")
		pdfFile.close()
		file = open(name[:-5]+".pdf","rb")
		st.download_button(label="Download PDF",data=file.read(),file_name=name[2:-5]+".pdf",mime="application/octet-stream")

elif onn1.toggle('PDF compressor feature un-complite now'):
# Read pdf into a list of DataFrame
	st.write("This feature can Compress your PDF file")
	place_holder=st.empty()
	with place_holder.form(key="form2"):
		uploaded_files = st.file_uploader("Choose a .PDF file (multiple files are not accepted)", accept_multiple_files=False)
		line=st.empty()
		submit_button = st.empty()
		if uploaded_files:
			name="./"+uploaded_files.name
			with open(name, "wb") as file:
				file.write(uploaded_files.getvalue())
			
	if submit_button.form_submit_button(label="Submit your choice"):
		name="./"+uploaded_files.name
		input_file = sys.argv[1]
		output_file = sys.argv[2]
		compress_file(name, name[:4]+" compress file.pdf")
		file = open(name[:4]+" compress file.pdf","rb")
		st.download_button(label="Download PDF",data=file.read(),file_name=name[:4]+" compress file.pdf",mime="application/octet-stream")
		
    
		
		

			
