window.addEventListener('DOMContentLoaded', (event) => {
    //gets list of buttons
    var button = document.getElementById("resetbutton");
    if (button != null){
        button.addEventListener('click', function(event) {
            //makes an HTTP request to /resetbudget
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
              if (this.readyState == 4 && this.status == 200) {
                  //changes number
                  location.reload(false)
              }
            };
            xhttp.open("GET", "/resetbudget", true);
            xhttp.send();
        })
    }
});