var loading_nodes
var pure_coors = []
var c = document.getElementById("canvas");
c.width = window.innerWidth;
c.height = window.innerHeight;
var ctx = c.getContext("2d");
ctx.fillStyle = "red";

var nodes_setup = () => {
    fetch("/leaderboard_setup")
        .then((response) => {
            return response.json();
        }).then((res) => {
            console.log(res);
            loading_nodes = res;
            draw_nodes(res);
        }).catch((error) => {
            console.log(error);
        })
}

var current_id = document.getElementById('id')
var current_owner = document.getElementById('owner')
var current_connections = document.getElementById('connections')
var current_points = document.getElementById('points')
var current_answer = document.getElementById('answer')
var form = document.getElementById("form");
var get_cash_fast = (arr) => {
    fetch("/info/" + arr)
        .then((response) => {
            return response.json();
        }).then((res) => {
            console.log(res);
            current_id.innerHTML = "Factory: " + res[0];
            current_owner.innerHTML = "Owner: " + res[1];
            current_connections.innerHTML = "Connections: " + res[2];
            current_answer.innerHTML = "Answer: " + res[3];
            current_points.innerHTML = "Points: " + res[4];
            form.style.opacity = '1';
        }).catch((error) => {
            console.log(error);
        })
}

const square_up = 100;
const padding = square_up - 10;
var draw_nodes = (arr) => {
    var x = 0; 
    var y = 0;
    for(var i = 0; i < arr.length; i++){
        let coordinates = []
        let coors = arr[i].split(' ');
        // console.log(coors);
        for (coor in coors){
            // console.log(coor);
            var nan = parseInt(coors[coor].split('')[1]);
            console.log(nan);
            coordinates.push(nan)
        }
        pure_coors.push(coordinates);
        x = coordinates[3] * square_up;
        y = coordinates[1] * square_up;
        //console.log(x + " " + y)
        ctx.fillRect(x, y, padding, padding);
    }
}

var comparison_search = () => {

}
c.addEventListener("click", (e) => {
    var mouseX = e.offsetX;
    var mouseY = e.offsetY;
    console.log('clicked: ' + mouseX + ' ' + mouseY)
    let standbyX = (mouseX - (mouseX%square_up))/square_up 
    let standbyY = (mouseY - (mouseY%square_up))/square_up 
    console.log('simplified: ' + standbyX + ' ' + standbyY)
    var search = [-1,-1,-1,-1];
    var search_id = -1;
    for (var i = 0; i < pure_coors.length; i++){
        if (pure_coors[i][1] == standbyY && pure_coors[i][3] == standbyX){
            
            if (mouseX < (pure_coors[i][3] * square_up) + padding && mouseY < (pure_coors[i][1] * square_up) + padding){
                console.log('inner')
                search = pure_coors[i]
                search_id = i;
                break;
            }
        }
    }
    console.log(search[3]  + " " + search[1])
    if (search_id > 0){
        get_cash_fast(loading_nodes[search_id])
    }
})

nodes_setup()