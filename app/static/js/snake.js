// Team Hair Investment Uncles :: Daniel He, Justin Mohabir, Sir, Alfred
// SoftDev pd2
// K30-- JS Paint
// 2023-04-24m
// --------------------------------------------------

var c = document.getElementById("slate");
var ctx = c.getContext("2d");
var requestID;

const x = 21;
let a = new Array(x); // create an empty array of length x
for (var i = 0; i < x; i++)
	 {
 		 a[i] = new Array(x); // make each element an array
	 }

for (var i = 0; i < x; i++)
	 {
     for (var j = 0; j < x; j++)
     	 {
         if(j==20 || j==0 || i==0 || i==20){
           a[i][j]=-1;
         }
         else {
           a[i][j]=0;
         }
     	 }
	 }
box_height=c.height/20;



ctx.beginPath();
ctx.fillStyle = "green";
ctx.fillRect(box_height * (3-1), box_height * (1-1), box_height, box_height);
ctx.stroke();

var wipeCanvas = () =>{
  ctx.clearRect(0, 0, 10000, 10000);
  for (var i = 0; i < x; i++) {
    ctx.beginPath();
    ctx.moveTo(0+i*box_height, 0);
    ctx.lineTo(0+i*box_height, c.height);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(0, 0+i*box_height);
    ctx.lineTo(c.width, 0+i*box_height);
    ctx.stroke();
  }
}

size=5;
x_change = 1;
y_change = 0;

x_pos=1;
y_pos=3;

var drawBoard = function() {
  wipeCanvas();
  for (var i = 1; i < x-1; i++)
  	 {
       for (var j = 1; j < x-1; j++)
       	 {
           if(a[i][j]>0){
            a[i][j]++;
           }

           if(a[i][j]>size){
            a[i][j]=0;
           }
       	 }
  	 }

     x_pos=x_pos+x_change;
     y_pos=y_pos+y_change;
     a[x_pos][y_pos]=1;

     for (var i = 1; i < x-1; i++)
  	 {
       for (var j = 1; j < x-1; j++)
       	 {
           if(a[i][j]>0){
             console.log()
             ctx.beginPath();
             ctx.fillStyle = "green";
             ctx.fillRect(box_height * (j-1), box_height * (i-1), box_height, box_height);
             ctx.stroke();
           }
       	 }
  	 }
  console.log(a);
}

spee=10;

var drawSnake = () => {
    //clear
    setTimeout(function () { 
      drawBoard();
      window.cancelAnimationFrame(requestID);
      requestID = window.requestAnimationFrame(drawSnake);
    }, 1000/spee)
  }
    

//var stopIt = function
var stopIt = () => {
    window.cancelAnimationFrame(requestID);
}

document.addEventListener('keydown', (event) => {
  var name = event.key;
  var code = event.code;
  console.log(name)

  if (name === 'w'){
      
      y_change=0
      x_change=-1
  }

  if (name === 's'){
      y_change=0
      x_change=1
  }
  
  if (name === 'd'){
      y_change=1
      x_change=0
  }

  if (name === 'a'){
      y_change=-1
      x_change=0
  }
  
}, false);

var startButton = document.getElementById("start");
startButton.addEventListener( "click", drawSnake);

console.log(a);
