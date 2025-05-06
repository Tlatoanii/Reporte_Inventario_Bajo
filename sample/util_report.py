from reportlab.platypus import Table
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer, KeepTogether, PageBreak, ListFlowable, ListItem
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from statistics import mode
from report import Reports


def validate_color(pendant, complete):
    det = int(complete/2)
    if pendant == 0:
        return colors.green
    elif pendant < det:
        return colors.orange
    else:
        return colors.red
    
def add_title_on_new_page(doc, title):
    styles= getSampleStyleSheet() 
    # Crear los elementos
    title_elements = [
        PageBreak(),
        Paragraph(title, styles['Heading2']),
    ]
        # Agregar cada elemento individualmente al documento
    for element in title_elements:
        doc.add_element(element)
    

def breakdown_tables(color, product_list, elements, product):
    column_widths = [85, 50, 50, 55, 55, 50, 45, 45, 100]
    font_size = 9
    doc_styles = getSampleStyleSheet()
    data_regular = [ [ "Estación", "Capacidad", "Alerta (%)","Registro (%)", "Registro (L)", "Inicio", "Fin", "Duración", "Observación" ] ]
    for station in product_list:
        initial_time = str(station['initial_time']).split(' ')[1]
        initial_time = f'{initial_time.split(':')[0]}:{initial_time.split(':')[1]}'
        final_time = str(station['final_time']).split(' ')[1]
        final_time = f'{final_time.split(':')[0]}:{final_time.split(':')[1]}'
        data_regular.append( [station['station'], '{:,} L'.format(int(station['tank_capacity'])), f'{station["per_limit"]} %', f'{station['min_per']} %', '{:,} L'.format(int(station['min_vol'])), f'{initial_time} h', f'{final_time} h', station['time_low'], station['note'] ] )
    
    table = Table(data_regular, colWidths= column_widths)
    style_regular = TableStyle([
        ("BACKGROUND", (0,0), (-1, 0), color),
        ("TEXTCOLOR", (0,0), (-1, 0), colors.whitesmoke),
        ("TEXTCOLOR", (-1, -1), (-1, -1), colors.black),
        ("ALIGN", (0,0), (-1, -1), "CENTER"),
        ("GRID", (0,0), (-1, -1), 1,  colors.black),
        ("FONTSIZE", (0, 0), (-1, -1), font_size)
    ])
    table.setStyle(style_regular)
    elements.append(Paragraph(product, doc_styles["Heading3"]))
    elements.append(table)
    return elements

def resume_table(doc, regular_list, premium_list, diesel_list, date):
    if len(regular_list) == 0 and len(premium_list) == 0 and len(diesel_list) == 0:
        return
    # date_title = str(date).split(' ')[0]
    doc_styles = getSampleStyleSheet()
    doc_title = Paragraph(str(date).split(' ')[0], doc_styles["Heading2"])
    spacer = Spacer(1,12)
    # [{'station': 'CAMINO REAL', 'initial_time': '2025-02-28 09:15:01', 'final_time': '2025-02-28 18:45:01', 'initial_per': '37.54', 'min_per': 21.1, 'initial_vol': '15714.62', 'min_vol': '8832.67', 'tank_capacity': '41861.0', 'time_low': '9:30:0'}
    elements = [doc_title]
    if len(regular_list) != 0:
        elements = breakdown_tables(colors.Color(0.18, 0.49, 0.20), regular_list, elements, "Regular")
    if len(premium_list) != 0:
        elements = breakdown_tables(colors.Color(0.78, 0.16, 0.16), premium_list, elements, "Premium")
    if len(diesel_list) != 0:
        elements = breakdown_tables(colors.Color(1.00, 0.56, 0.00), diesel_list, elements, "Diesel")
    elements.append(spacer)
    doc.add_element(KeepTogether(elements))

def list_bad_lecture(bad_lecture, doc):
    bullet_style = doc.justify_paragraph()
    styles = getSampleStyleSheet()
    list_items = []
    if len(bad_lecture) != 0:
        for station in bad_lecture:
            list_items.append(ListItem(Paragraph(f'{station['station'].title()}: Presentó lecturas en ceros {"1 vez" if station['times_appeared'] == 1 else f'{station['times_appeared']} veces en el mes' }', bullet_style)))
    else: 
        list_items.append(ListItem(Paragraph(f'Ninguna estación presento lecturas en ceros', bullet_style)))
    bullet_list = ListFlowable(list_items, bulletType='bullet')
    doc.add_element(KeepTogether([Paragraph("Malas Capturas", styles['Heading3']), Paragraph("Capturas que enviaron registros en ceros en Monitor System debido a problemas de la estación o externos", bullet_style), bullet_list]))

def table_station_alert(station, color):
    column_widths = [85, 50, 50]
    font_size = 9
    data_table = [["Estación", "Fecha", "Hora Alerta"]]
    for date in station['dates']:
        data_table.append([station['station'], date.split(' ')[0], f'{date.split(' ')[1].split(':')[0]}:{date.split(' ')[1].split(':')[1]} hrs'])
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

def get_general_statistics(doc: Reports, product_list, color):
    bullet_style = doc.justify_paragraph()
    list_items = []
    for station in product_list:
        if station['times_appeared'] == 1:
            group = KeepTogether([
                Paragraph(f"-    <b>{station['station'].title()}</b>: Presentó <b>{station['times_appeared']}</b> alerta de nivel bajo de combustible el día {station['dates'][0].split(' ')[0]} a las {station['dates'][0].split(' ')[1].split(':')[0]}:{station['dates'][0].split(' ')[1].split(':')[1]} hrs, correspondiente al mes", bullet_style ), 
                Spacer(1, 12), 
                table_station_alert(station, color), 
                Spacer(1, 12)
            ])
            doc.add_element(group)
        elif station['times_appeared'] == 2:
            group = KeepTogether([
                Paragraph(f"-   <b>{station['station'].title()}</b>: Presentó <b>{station['times_appeared']}</b> alertas de nivel bajo de combustible los dias {station['dates'][0].split(' ')[0]} y  {station['dates'][1].split(' ')[0]} a las {station['dates'][0].split(' ')[1].split(':')[0]}:{station['dates'][0].split(' ')[1].split(':')[1]} hrs y {station['dates'][1].split(' ')[1].split(':')[0]}:{station['dates'][0].split(' ')[1].split(':')[1]} hrs, correspondientes al mes", bullet_style),
                Spacer(1,12), 
                table_station_alert(station, color), 
                Spacer(1,12)
            ])
            doc.add_element(group)
        elif station['times_appeared'] > 2:
            station['dates'] = sorted(station['dates'])
            mode_date = mode(station['dates'])
            group = KeepTogether([
                Paragraph(f"-    <b>{station['station'].title()}</b>: Presentó <b>{station['times_appeared']}</b> alertas de nivel bajo de combustible, en la <b>moda</b> la estación presento estás alertas a las <b>{mode_date.split(' ')[1].split(':')[0]}:{mode_date.split(' ')[1].split(':')[1]} hrs</b>, del correspondiente mes", bullet_style),
                Spacer(1,12), 
                table_station_alert(station, color), 
                Spacer(1,12)
            ])
            doc.add_element(group)
    return list_items


def stations_resume(doc: Reports, list_regular, list_premium, list_diesel):
    if len(list_regular) == 0 and len(list_premium) == 0 and len(list_diesel) == 0:
        return
    styles = getSampleStyleSheet()
    doc.add_element(Paragraph("Resúmen por producto", styles['Heading2']))
    if len(list_regular) != 0:
        doc.add_element(Paragraph("Regular", styles['Heading3']))
        get_general_statistics(doc, list_regular, colors.Color(0.18, 0.49, 0.20))
    if len(list_premium) != 0:
        doc.add_element(Paragraph("Premium", styles['Heading3']))
        get_general_statistics(doc, list_premium, colors.Color(0.78, 0.16, 0.16))
    if len(list_diesel) != 0:
        doc.add_element(Paragraph("Diesel", styles['Heading3']))
        get_general_statistics(doc, list_diesel, colors.Color(1.00, 0.56, 0.00))

def general_table(list_product, color):
    font_size = 9
    column_widths = [      85     ,     50    ,      50     ,       55     ,       55      ,    100   ,   100 ,     45    ]
    data_regular = [ [ "Estación", "Capacidad", "Alerta (%)","Registro (%)", "Registro (L)", "Fecha Inicio", "Fecha Fin", "Duración"] ]
    for product in list_product:
        data_regular.append( [product['station'], '{:,} L'.format(int(product['tank_capacity'])), f'{product["per_limit"]} %', f'{product['min_per']} %', '{:,} L'.format(int(product['min_vol'])), product['initial_time'], product['final_time'], product['time_low'] ] )
    
    table = Table(data_regular, colWidths= column_widths)
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

def station_resume_data(station_store, regular_station, premium_station, diesel_station, report: Reports):
    try: 
        styles = getSampleStyleSheet()
        for index, station in enumerate(station_store):
            if( len(regular_station[index]) == 0 and len(premium_station[index]) == 0 and len(diesel_station[index]) == 0 ):
                continue
            station = Paragraph(station, styles['Heading2'])
            if len(regular_station[index]) != 0:
                station_product = Paragraph("REGULAR", styles['Heading3'])
                table_regular = general_table(regular_station[index], colors.Color(0.18, 0.49, 0.20))
                report.add_element(KeepTogether( [station, station_product, Spacer(1, 12), table_regular, Spacer(1, 12)] ))
            if len(premium_station[index]) != 0:
                station_product = Paragraph("PREMIUM", styles['Heading3'])
                table_premium = general_table(premium_station[index], colors.Color(0.78, 0.16, 0.16))
                report.add_element(KeepTogether( [station, station_product, Spacer(1, 12), table_premium, Spacer(1, 12)] ))
            if len(diesel_station[index]) != 0:
                station_product = Paragraph("DIESEL", styles['Heading3'])
                table_diesel = general_table(diesel_station[index], colors.Color(1.00, 0.56, 0.00))
                report.add_element(KeepTogether( [station, station_product, Spacer(1, 12), table_diesel, Spacer(1, 12)] ))
    except Exception as e: 
        print(f'Error al generar tabla de resumen por estacion: {e}')