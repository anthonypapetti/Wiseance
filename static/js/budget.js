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
                  var new_money = this.responseText.slice(1, -2)
                  console.log(new_money)
                  console.log(this.responseText)
                  var moneytag = document.getElementById("money")
                  moneytag.innerText = new_money
              }
            };
            xhttp.open("GET", "/resetbudget", true);
            xhttp.send();
        })
    }
});