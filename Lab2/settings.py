SETTINGS = {
    "IP":"87.245.198.147",
    "COST":2,
    "input_filename":"traffic.csv"
}

input_filename = "G:\Stepa\Учёба\УМУ\Лаб 3\Счет_шаблон1.html"

with open(input_filename, 'r', encoding='utf-8') as f:
    html = f.read()

template = Template(html)
output = template.render(context=context)

with open(name, 'wb') as f:
    f.write(output.encode('utf-8'))

options = {
    'page-size': 'A4',
    'margin-top': '2cm',
    'margin-left': '3cm',
    'margin-right': '2cm'
}

pdfkit.from_file(name, context['stamp'], options=options)
os.remove(name)