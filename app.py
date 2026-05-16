import streamlit as st
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class GTUReport(FPDF):
    def header(self):
        # --- STATIC MULTI-LINE COMPOSITE BOX BORDER ---
        self.set_line_width(0.2)
        self.rect(4.5, 4.5, 201, 288) # Outer accent
        self.set_line_width(1.2) 
        self.rect(5.5, 5.5, 199, 286) # Main Bold Frame
        self.set_line_width(0.2)
        self.rect(6.8, 6.8, 196.4, 283.4) # Inner accent
        
        # --- INSTITUTIONAL HEADER ELEMENTS ---
        self.set_y(15)
        self.set_font("times", "", 12)
        self.cell(0, 6, "Sardar Vallabhbhai Education Society's", 
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.set_font("times", "B", 18)
        self.cell(0, 10, "R. N. G. PATEL INSTITUTE OF TECHNOLOGY", 
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.set_font("times", "", 11)
        self.cell(0, 5, "ISROLI, BARDOLI - 394620", 
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        
        self.ln(5)
        self.set_font("times", "B", 14)
        self.cell(0, 7, "COMPUTER SCIENCE AND ENGINEERING DEPARTMENT", 
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.set_font("times", "B", 16)
        self.cell(0, 10, "PRACTICAL / TERM-WORK REPORT", 
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

def generate_pdf_bytes(data):
    pdf = GTUReport()
    pdf.add_page()
    pdf.set_font("times", "", 12)
    pdf.set_line_width(0.2)

    # ==========================================
    # 1. FIXED TEMPLATE STRUCTURE BLOCK (GROUNDED)
    # ==========================================
    
    # Row: TERM (Sits below centered title, right aligned)
    pdf.set_y(58)
    pdf.set_x(155)
    pdf.set_font("times", "B", 12)
    pdf.write(10, "TERM: ")
    
    # Row: Subject
    pdf.set_y(70)
    pdf.set_x(20)
    pdf.set_font("times", "", 12)
    pdf.write(10, "Subject : ")
    pdf.line(40, 78, 195, 78) 
    
    # Row: PEN & Semester
    pdf.set_y(82)
    pdf.set_x(20)
    pdf.write(10, "PEN : ")
    pdf.line(34, 90, 135, 90)
    
    pdf.set_x(145)
    pdf.write(10, "Semester : ")
    pdf.line(166, 90, 195, 90)
    
    # Row: Name of Student
    pdf.set_y(94)
    pdf.set_x(20)
    pdf.write(10, "Name of Student : ")
    pdf.line(53, 102, 195, 102)
    
    # Row: Class & Batch
    pdf.set_y(106)
    pdf.set_x(20)
    pdf.write(10, "Class : ")
    pdf.line(34, 114, 135, 114)
    
    pdf.set_x(145)
    pdf.write(10, "Batch : ")
    pdf.line(160, 114, 195, 114)
    
    # Row: Title of Experiment
    pdf.set_y(118)
    pdf.set_x(20)
    pdf.write(10, "Name of Experiment / Title of Term Work : ")
    title_start_x = pdf.get_x()
    
    # Grounded Static Lines layout mapped to Image Template
    pdf.line(title_start_x, 126, 195, 126) # Line 1 (Starts after text)
    pdf.line(20, 136, 195, 136)            # Line 2 (Full Width back to left margin)
    pdf.line(20, 146, 195, 146)            # Line 3 (Full Width back to left margin)

    # ==========================================
    # 2. SEPARATE DYNAMIC DATA OVERLAY BLOCK
    # ==========================================
    pdf.set_font("times", "", 12) 

    # Overlapping value over TERM
    pdf.set_y(58)
    pdf.set_x(171)
    pdf.cell(24, 10, str(data['term']), align='L')

    # Overlapping value over Subject
    pdf.set_y(70)
    pdf.set_x(42)
    pdf.cell(151, 10, str(data['subject']), align='L')
    
    # Overlapping value over PEN
    pdf.set_y(82)
    pdf.set_x(36)
    pdf.cell(97, 10, str(data['pen']), align='L')
    
    # Overlapping value over Semester
    pdf.set_y(82)
    pdf.set_x(168)
    pdf.cell(25, 10, str(data['sem']), align='L')
    
    # Overlapping value over Name of Student
    pdf.set_y(94)
    pdf.set_x(55)
    pdf.cell(138, 10, str(data['name']), align='L')
    
    # Overlapping value over Class
    pdf.set_y(106)
    pdf.set_x(36)
    pdf.cell(97, 10, str(data['cls']), align='L')
    
    # Overlapping value over Batch
    pdf.set_y(106)
    pdf.set_x(162)
    pdf.cell(31, 10, str(data['batch']), align='L')
    
    # --- TEXT SPLITTING SYSTEM ---
    words = data['title'].split(' ')
    line_data = ["", "", ""]
    idx = 0
    
    for word in words:
        avail_width = (195 - title_start_x) if idx == 0 else 175 
        
        while pdf.get_string_width(word) > (avail_width - 4):
            chop_idx = 0
            while chop_idx < len(word) and pdf.get_string_width(word[:chop_idx+1]) < (avail_width - 4):
                chop_idx += 1
            line_data[idx] += word[:chop_idx]
            word = word[chop_idx:]
            if idx < 2:
                idx += 1
                avail_width = 175
                
        if pdf.get_string_width(line_data[idx] + word + " ") < (avail_width - 2):
            line_data
