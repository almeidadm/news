document.addEventListener('DOMContentLoaded', function() {
    const mapaContainer = document.getElementById('mapa-nucleos');
    
    if (mapaContainer) {
        try {
            const rawData = document.getElementById('lista-de-nucleos').dataset.nucleos;
            const decodedData = new DOMParser().parseFromString(rawData, 'text/html').body.textContent;
            const nucleosData = JSON.parse(decodedData);
            
            const map = L.map('mapa-nucleos').setView([-23.69, -45.42], 10);
            
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);

            const validMarkers = nucleosData.filter(nucleo => 
                nucleo.localizacao?.latitude && nucleo.localizacao?.longitude
            );

            if (validMarkers.length === 0) {
                throw new Error('Nenhuma localização válida encontrada');
            }

            const markers = validMarkers.map(nucleo => {
                const marker = L.marker([nucleo.localizacao.latitude, nucleo.localizacao.longitude]);
                marker.bindPopup(`
                    <b>${nucleo.nome}</b><br>
                    <small>${nucleo.endereco}</small><br>
                    <hr>
                    <strong>Horários:</strong> ${nucleo.horarios}<br>
                    <strong>Professor:</strong> ${nucleo.professor.nome}<br>
                    <strong>Contato:</strong> ${nucleo.professor.contato || 'N/A'}
                `);
                return marker;
            });

            const markerGroup = L.featureGroup(markers).addTo(map);
            map.fitBounds(markerGroup.getBounds().pad(0.2));
            
        } catch (error) {
            mapaContainer.innerHTML = `
                <div class="map-error">
                    Não foi possível carregar o mapa: ${error.message}
                </div>
            `;
            console.error('Erro no mapa:', error);
        }
    }
});