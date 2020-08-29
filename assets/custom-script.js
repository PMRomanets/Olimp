//alert('If you see this alert, then your custom JavaScript script has run!')


function show() {

    elem = document.getElementById("show-hide-more");

	elem.style.display = 'block';
	elem.style.visibility = 'visible';

};

function showHourPop(date_str, id){

//  app.scripts.append_script 

    //alert(id);

    var x = document.getElementById("pop-div");

    if (x.style.display === "none") {

        x.style.display = "block";
        x.style.visibility = "visible";


        x.innerHTML = '<button type="button" onclick="closePop()">Close</button><iframe src="../traffic_by_hour_pop_graph?date=' + date_str + '&id=' + id + '"></iframe>';

    } else {
        x.style.display = "none";
    }

}


function closePop(){

    var x = document.getElementById("pop-div");

    x.style.display = "none";


}