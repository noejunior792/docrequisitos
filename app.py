from flask import Flask, render_template, request
import folium
from geopy.geocoders import Nominatim

app = Flask(__name__)

# Dados fictícios de documentos e localizações
document_data = {
    'passaporte': {'title': 'Página do Passaporte', 'location_required': True},
    'bilhete de identidade': {'title': 'Bilhete de identidade', 'location_required': True},
    'rg': {'title': 'Página do RG', 'location_required': False},
    'cnh': {'title': 'Página da CNH', 'location_required': False}
}

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para a pesquisa de documentos
@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['searchTerm'].lower()

    if search_term in document_data:
        document = document_data[search_term]
        return render_template('passaporte.html', document=document)
    else:
        return render_template('not_found.html')
    
    
# Rota para a página do passaporte com localização fictícia
@app.route('/passaporte', methods=['GET', 'POST'])
def passaporte():
    if request.method == 'POST':
        location_name = request.form['locationName']

        # Utilizar geopy para obter as coordenadas da localização pelo nome
        geolocator = Nominatim(user_agent="my_geocoder")
        location = geolocator.geocode(location_name)

        if location:
            latitude, longitude = location.latitude, location.longitude

            # Criação do mapa com Folium
            map_passaporte = folium.Map(location=[latitude, longitude], zoom_start=15)
            folium.Marker([latitude, longitude], popup=f'Localização: {location_name}').add_to(map_passaporte)

            # Salvando o mapa como um arquivo HTML temporário
            map_passaporte.save("templates/map_passaporte.html")

            return render_template('passaporte.html', map_passaporte='map_passaporte.html', location_name=location_name)

    return render_template('passaporte.html', map_passaporte=None, location_name=None)

if __name__ == '__main__':
    app.run(debug=True)
