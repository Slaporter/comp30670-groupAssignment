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
