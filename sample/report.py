from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime

class Reports:
    
    tables = []
    doc_elements = []
    
    def __init__(self):
        current_date = datetime.now().strftime("%d-%m-%Y")
        doc_styles = getSampleStyleSheet()
        doc_title = Paragraph("Reporte Nivel Bajo de Inventarios", doc_styles["Title"])
        doc_header = Paragraph(
            f"""La siguiente tabla presenta los registros de nivel de un tanque de almacenamiento de gran capacidad. Se incluyen datos relevantes para el monitoreo y análisis de los niveles de inventario,
            permitiendo identificar eventos de bajo volumen y su tiempo de resolución. Se incluyen gráficas que expresan cuántos días en el mes una estación presentó niveles bajos de combustible y, 
            al final, un resumen general por producto y estación.""")
        
        self.doc_elements.append(doc_title)
        self.doc_elements.append(Spacer(1,12))
        self.doc_elements.append(doc_header)
        # self.doc_elements.append(Spacer(1, 24))
        
    def add_element(self, element):
        self.doc_elements.append(element)
        
    def add_element_at_first(self, element):
        self.doc_elements.insert(3, element)
    
    def justify_paragraph(self):
        justified_style = ParagraphStyle(
            name="Justified",
            parent= getSampleStyleSheet()["Normal"],
            alignment=4, 
            fontSize=11,
            leading=15  
        )
        return justified_style
    
    def createReport(self):
        pdf_name = "docs/ReporteInventarioBajo.pdf"
        document = SimpleDocTemplate(pdf_name, pagesize= letter)
        document.build(self.doc_elements)