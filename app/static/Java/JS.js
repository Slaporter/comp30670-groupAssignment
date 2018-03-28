//Map with marker
function myMap() {

    var myLongitude = {
        lat: 53.3498,
        lng: -6.2603
    };
    var map = new google.maps.Map(document.getElementById("map"), {
        center: myLongitude,
        zoom: 14
    });

    var marker = new google.maps.Marker({
        position: myLongitude,
        map: map
    });
}

{% for stop in stops %}
function markers(){	
	posit= {
		lat: {{ stop[0] }},
		lng: {{ stop[1] }}
		};

var map = new google.maps.Map(document.getElementById("map"), {
    centre: myLongitude
    zoom: 14
});
var marker = new google.maps.Marker({
    position: posit,
    map: map
});
markers.push(marker);
}
{% endfor %}
