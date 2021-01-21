function initMap() {
    var options = {
        zoom: 10,
        center: { lat: 40.730610, lng: -73.935242 } //Coordinates of New York 
    }
    var map = new google.maps.Map(document.getElementById('map'), options);

    function addMarker(prop) {
        var marker = new google.maps.Marker({
            position: prop.coordinates, // Passing the coordinates
            map: map, //Map that we need to add
            draggarble: false// If set to true you can drag the marker
        });

        if (prop.iconImage) { marker.setIcon(prop.iconImage); }
        if (prop.content) {
            var information = new google.maps.InfoWindow({
                content: prop.content
            });

            marker.addListener('click', function () {
                information.open(map, marker);
            });
        }
    }

    addMarker({
        coordinates: { lat: 40.6782, lng: -73.9442 },
        iconImage: 'https://img.icons8.com/fluent/48/000000/marker-storm.png',
        content: '<h4>Brooklyn Marker</h4>'
    });

    addMarker({ coordinates: { lat: 40.7831, lng: -73.9712 } }); // Manhattan Coordinates

}
