//{"coord":{"lon":-6.26,"lat":53.35},"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04d"}],"base":"stations","main":{"temp":280.15,"pressure":1010,"humidity":93,"temp_min":280.15,"temp_max":280.15},"visibility":10000,"wind":{"speed":6.7,"deg":50},"clouds":{"all":75},"dt":1523448000,"sys":{"type":1,"id":5237,"message":0.0029,"country":"IE","sunrise":1523424834,"sunset":1523474349},"id":2964574,"name":"Dublin","cod":200}

function standardDay(value) {
    var xmlhttp = new XMLHttpRequest();
    console.log('Value = ', value);
    var url = "http://api.openweathermap.org/data/2.5/weather?APPID=52b3fcc8ca94382baa1747a7dde59108&q=Dublin"
;


    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
             var parsedObj = JSON.parse(xmlhttp.responseText);
            console.log(parsedObj[4]);
             myFunction(parsedObj,value);
        }
    };
    
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

//David Coyle Lecture 11- https://csmoodle.ucd.ie/moodle/pluginfile.php/86873/mod_resource/content/1/Lecture%2011%20-%20JSON.pdf
    
function myFunction(obj,value){

    var out = "";
    var days = parseInt(value);
    
    for(i = 0; i < days; i++) {
        out += "<h8> DAY" + (i+1) + "</h8><table class = 'table1'> <tr class = 'icon'><td>" + "<img style= 'width:40%; height:150px' src = 'http://openweathermap.org/img/w/" + obj.list[i].weather[0].icon + ".png' </td></tr> <tr><td> <h7> The " + (i+19) + "th of October 2017 </h7> </td></tr><tr><td> " + obj.list[i].weather[0].description + "</td></tr><tr><td> Cloudiness " + obj.list[i].clouds + "%<tr><td> Minimum Temperature " + obj.list[i].temp + "&degC</td></tr>"
        + "<tr><td> Maximum Temperature " + obj.list[i].temp.max + "&degC</td></tr></table><br>";

   document.getElementById("days").innerHTML = out;
    
}
}




