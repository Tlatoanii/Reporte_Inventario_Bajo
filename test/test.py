from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer, KeepTogether, PageBreak, ListFlowable, ListItem
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("test.pdf")
styles = getSampleStyleSheet()
list_items = []
bullet_style = styles['Normal']
i = 0

def table_station_alert(station, color):
    column_widths = [70, 50, 50]
    font_size = 9
    data_table = [["Estación", "Fecha", "Hora Alerta"], ["ESTACIÓN 1", "2025-03-24", "09:00:00"]]
    table = Table(data_table, colWidths= column_widths)
    style_regular = TableStyle([
        ("BACKGROUND", (0,0), (-1, 0), color),
        ("TEXTCOLOR", (0,0), (-1, 0), colors.whitesmoke),
        ("TEXTCOLOR", (-1, -1), (-1, -1), colors.black),
        ("ALIGN", (0,0), (-1, -1), "CENTER"),
        ("GRID", (0,0), (-1, -1), 1,  colors.black),
        ("FONTSIZE", (0, 0), (-1, -1), font_size)
    ])
    table.setStyle(style_regular)
    return table

for i in range(9):
    group = KeepTogether([
        Paragraph("Ejemplo de texto", bullet_style),
        Spacer(1, 12),
        table_station_alert("ESTACIÓN", colors.Color(0.18, 0.49, 0.20))
    ])
    list_items.append(ListItem(group))
bullet_list = ListFlowable(list_items, bulletType='bullet')

doc.build([bullet_list])