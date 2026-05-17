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
            line_data[idx] += word + " "
        elif idx < 2:
            idx += 1
            line_data[idx] += word + " "

    # Float clean layout text arrays across the dynamic segments
    pdf.set_y(118)
    pdf.set_x(title_start_x + 2)
    pdf.cell(195 - title_start_x - 2, 10, line_data[0].strip(), align='L')
    
    pdf.set_y(128)
    pdf.set_x(22) 
    pdf.cell(173, 10, line_data[1].strip(), align='L')
    
    pdf.set_y(138)
    pdf.set_x(22) 
    pdf.cell(173, 10, line_data[2].strip(), align='L')

    # ==========================================
    # 3. FIXED LOWER TRACKING COLUMN SYSTEM
    # ==========================================
    
    def render_aligned_row(label_text, value_text, y_pos):
        pdf.set_y(y_pos - 8)
        pdf.set_x(20)
        pdf.cell(118, 10, label_text, align='R')
        pdf.line(138, y_pos, 195, y_pos)
        pdf.set_x(138)
        pdf.cell(57, 10, str(value_text), align='C')

    render_aligned_row("Practical / Term Work No. : ", data['work_no'], 168)
    render_aligned_row("Conducted On : ", "    /       /    ", 177)
    render_aligned_row("Date of Submission : ", "    /       /    ", 186)
    render_aligned_row("Actual Date of Submission : ", "    /       /    ", 195)

    # Checked By & Remarks Rows
    pdf.set_y(210)
    pdf.set_x(20)
    pdf.write(10, "Checked By : ")
    pdf.line(46, 218, 195, 218)
    pdf.set_x(48)
    pdf.cell(147, 10, str(data['faculty']), align='L')
    
    pdf.set_y(222)
    pdf.set_x(20)
    pdf.write(10, "Remarks : ")
    pdf.line(41, 230, 195, 230)

    # --- FOOTER BLOCK ---
    footer_y = 255
    pdf.set_y(footer_y - 8)
    
    # Signature
    pdf.set_x(20)
    pdf.write(10, "Signature : ")
    pdf.line(43, footer_y, 85, footer_y)
    
    # Date
    pdf.set_x(90)
    pdf.write(10, "Date: ")
    pdf.line(102, footer_y, 142, footer_y)
    pdf.set_x(102)
    pdf.cell(40, 10, "   /   /", align='C')
    
    # Marks
    pdf.set_x(147)
    pdf.write(10, "Marks : ")
    pdf.line(162, footer_y, 195, footer_y)

    # Return output safely wrapped as crisp binary bytes
    return bytes(pdf.output())

# --- STREAMLIT WEB APP UI ---
st.set_page_config(page_title="GTU Report Generator", page_icon="📄", layout="centered")
st.title("📄 Practical / Term-Work Report Generator")
st.write("Fill out the details below to generate a perfectly aligned document.")

# UI CHANGE: This renders immediately when the page loads, before anyone submits details!
st.link_button(
    label="📸 Connect with me on Instagram (@sohammistry_176)",
    url="https://www.instagram.com/sohammistry_176",
    use_container_width=True
)
st.write("") # Quick vertical spacing element

with st.form("report_form"):
    st.subheader("Common Institutional Info")
    col1, col2 = st.columns(2)
    with col1:
        term = st.text_input("TERM", placeholder="e.g., 252")
        subject = st.text_input("Subject Title", placeholder="e.g., OPERATING SYSTEMS(1CS401)")
        pen = st.text_input("PEN (Enrollment Number)", placeholder="e.g., 250843131014")
        name = st.text_input("Student Name", placeholder="e.g., Mistry SohamKumar Bharatbhai")
    with col2:
        sem = st.text_input("Semester", placeholder="e.g., 4")
        cls = st.text_input("Class", placeholder="e.g., CSE 24-B")
        batch = st.text_input("Batch", placeholder="e.g., 244")
        faculty = st.text_input("Faculty Member (Checked By)", placeholder="e.g., Mr. Xyz Abc Pqr")
        
    st.subheader("Report Specific Assignment Details")
    work_no = st.text_input("Practical / Term Work No.", placeholder="e.g., 27")
    title = st.text_area("Experiment / Assignment Title", placeholder="e.g., Study of various features of O.S and its types.")

    submitted = st.form_submit_button("Compile & Verify Layout")

# Renders selectively only when processing active entries
if submitted:
    if not work_no or not title:
        st.error("Please fill in at least the 'Work No' and 'Experiment Title' to generate a file.")
    else:
        payload = {
            "term": term, "subject": subject, "pen": pen, "name": name,
            "sem": sem, "cls": cls, "batch": batch, "faculty": faculty,
            "work_no": work_no, "title": title
        }
        
        with st.spinner("Compiling document layers..."):
            pdf_bytes = generate_pdf_bytes(payload)
        
        st.success("🎉 Layout Compiled Successfully!")
        st.download_button(
            label="⬇️ Download PDF Report",
            data=pdf_bytes,
            file_name=f"Term_Work_{work_no}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
