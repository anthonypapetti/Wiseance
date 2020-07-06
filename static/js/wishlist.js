function getChildById(parent, id) {
    children = parent.children
    for (var i = 0; i < children.length; i++) {
        if (children[i].id == id) {
            return children[i]
        }
    }
}

window.addEventListener('DOMContentLoaded', (event) => {
    //gets list of buttons
    var buttons = document.getElementsByClassName("fa-trash-o");
    for (let i = 0; i < buttons.length; i++) {
        console.log(buttons[i]);
        //adds event listener to each button
        buttons[i].addEventListener('click', function(event) {
            //this function makes an HTTP request to /deleteamazon
            //then removes the row
            //gets title
            button = event.originalTarget.parentElement
            console.log(button.parentElement)
            title = getChildById(button.parentElement, "title")

            console.log(title.innerText)
            //HTTP request
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
              if (this.readyState == 4 && this.status == 200) {
                  //removes row
               title.parentElement.remove()
              }
            };
            xhttp.open("GET", "/deleteamazon?name=" + title.innerText, true);
            xhttp.send();
        });
    }
});