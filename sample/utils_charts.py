import matplotlib.pyplot as plt
from reportlab.platypus import Paragraph,Spacer, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet

def stadistics_graph(data, product, month, color, doc = None):
	sorted_data = sorted(data, key=lambda stations: stations['times_appeared'] ) 
	# Obtener los nombres de las estaciones
	plty = [station['station'] for station in sorted_data]
	# Ejemplo de gráfico
	fig, ax = plt.subplots()
	ax.barh(plty, [station['times_appeared'] for station in sorted_data], color= color)
	plt.xlabel(f"# de Días con poco producto en {month}")
	plt.title(f"{product} - {month}" )
	plt.tight_layout()
	plt.savefig(f'res/{product}_chart', dpi=300)
	plt.close()
	# plt.show()
	if (doc != None):
		styles = getSampleStyleSheet()
		elements = []
		elements.append(Paragraph(f"Estadisticas de producto bajo en {product}", styles['Heading3']))
		elements.append(Spacer(1,12))
		elements.append(Image(f'res/{product}_chart.png', width=500, height=300))
		doc.add_element_at_first(KeepTogether(elements))


if __name__ == "__main__":
    stadistics_graph([{'station': 'SERVIOK', 'times_appeared': 5, 'times_low': ['3:30 h', '2:0 h', '9:29 h', '9:0 h', '3:29 h']},
        {'station': 'COLIBRI', 'times_appeared': 2, 'times_low': ['4:59 h', '9:0 h']}, 
        {'station': 'SMART', 'times_appeared': 5, 'times_low': ['4:59 h', '0:30 h', '5:29 h', '8:0 h', '6:0 h']},
        {'station': 'CAMINO REAL', 'times_appeared': 5, 'times_low': ['9:30 h', '7:0 h', '9:30 h', '3:29 h', '9:30 h']},
        {'station': 'OKTAN EKO', 'times_appeared': 3, 'times_low': ['5:30 h', '5:30 h', '0:59 h']},
        {'station': 'DIEGO', 'times_appeared': 1, 'times_low': ['1:0 h']},
        {'station': 'GRIÑON', 'times_appeared': 6, 'times_low': ['6:0 h', '1:0 h', '8:30 h', '2:30 h', '3:30 h', '1:30 h']},
        {'station': 'MAYORAZGO', 'times_appeared': 2, 'times_low': ['5:0 h', '2:30 h']},
        {'station': 'FERALGO', 'times_appeared': 1, 'times_low': ['0:30 h']},
        {'station': 'ACATEPEC 2', 'times_appeared': 1, 'times_low': ['5:29 h']}], "Regular", "Febrero", "darkgreen")