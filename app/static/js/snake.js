
var c = document.getElementById("slate");
var ctx = c.getContext("2d");
var requestID;

const x = 22;
let a = new Array(x); // create an empty array of length x
for (var i = 0; i < x; i++)
	 {
 		 a[i] = new Array(x); // make each element an array
	 }

const box_height=c.height/20;



var wipeCanvas = () =>{
  ctx.clearRect(0, 0, 10000, 10000);
  ctx.strokeStyle = "white";
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

wipeCanvas();
var isSetup=false;
var size;
var xChange;
var yChange;

var xPos;
var yPos;

var fruitX;
var fruitY;

var isPlaying;
var isShuffled;

var randomNumber = () =>{
	return Math.floor(Math.random() * 20) + 1;
}


var setup = () =>{
	//clears the array
	keys=['w','a','s','d'];
	up.innerHTML="Up: " + keys[0];
	down.innerHTML="Down: " + keys[2];
	left.innerHTML="Left: " + keys[1];
	right.innerHTML="Right: " + keys[3];
	isShuffled=false;
	for (var i = 0; i < x; i++)
		 {
	     for (var j = 0; j < x; j++)
	     	 {
	         if(j==21 || j==0 || i==0 || i==21){
	           a[i][j]=-1;
	         }
	         else {
	           a[i][j]=0;
	         }
	     	 }
		 }
	isSetup=true;
	size=1;
	xChange = 1;
	yChange = 0;

	xPos=Math.floor(Math.random() * 10) + 5
	yPos=Math.floor(Math.random() * 10) + 5

	while(fruitX != xPos && fruitY !=yPos){
		fruitX=randomNumber();
		fruitY=randomNumber();
	}

	a[fruitX][fruitY]=-2;

	isPlaying = true;
}


//Beeg function
var drawBoard = function() {
  wipeCanvas();
	//increment the values on the board
  for (var i = 1; i < x-1; i++)
  	 {
       for (var j = 1; j < x-1; j++)
       	 {
           if(a[i][j]>0){
            a[i][j]++;
           }
					 //check if any go above the size req
           if(a[i][j]>size){
            a[i][j]=0;
           }
       	 }
  	 }

     xPos=xPos+xChange;
     yPos=yPos+yChange;

		 // in the case of losing
		 if(a[xPos][yPos]===-1 || a[xPos][yPos]>0 ){
			 window.cancelAnimationFrame(requestID);
			 isPlaying=false;
			 isSetup=false;
			 if(size<3){
				 scoreMessage.innerHTML = "You get no score";
			 } else {
				 scoreMessage.innerHTML = "You get this score: " + (size-2).toString();
				 document.getElementById('snakeInput').value = size-2;
				 document.getElementById('snakeForm').submit();
			 }
			 scoreMessage.innerHTML
			 return;
		 }

		 //froot
		 if(a[xPos][yPos]===-2){
			 size++;
			 fruitX=randomNumber();
			 fruitY=randomNumber();
			 while(a[fruitX][fruitY]>0 && a[fruitX][fruitY]!=-2){
		 		fruitX=randomNumber();
		 		fruitY=randomNumber();
		 	}
			 a[fruitX][fruitY]=-2;
			 if(!isShuffled){
				 shuffle(keys);
				 up.innerHTML="Up: " + keys[0];
				 down.innerHTML="Down: " + keys[2];
				 left.innerHTML="Left: " + keys[1];
				 right.innerHTML="Right: " + keys[3];
			 }
		 }


     a[xPos][yPos]=1;

		 //render board
     for (var i = 1; i < x-1; i++)
  	 {
       for (var j = 1; j < x-1; j++)
       	 {
           if(a[i][j]>0){
             ctx.beginPath();
             ctx.fillStyle = "green";
             ctx.fillRect(box_height * (j-1), box_height * (i-1), box_height, box_height);
             ctx.stroke();
           }

					 if(a[i][j]===-2){
             ctx.beginPath();
             ctx.fillStyle = "red";
             ctx.fillRect(box_height * (j-1), box_height * (i-1), box_height, box_height);
             ctx.stroke();
           }
       	 }
  	 }
}

spee=10;

var drawSnake = () => {
    //clear
		if(!isSetup){
			setup();
		}
		if (isPlaying){
			setTimeout(function () {
	      drawBoard();
				if(!isSetup){
					wipeCanvas();
					return;
				}
	      window.cancelAnimationFrame(requestID);
	      requestID = window.requestAnimationFrame(drawSnake);
	    }, 1000/spee)
		}
  }

function shuffle(array) {
	let currentIndex = array.length
	let randomIndex;

	// While there remain elements to shuffle.
	while (currentIndex != 0) {
		// Pick a remaining element.
		randomIndex = Math.floor(Math.random() * currentIndex);
		currentIndex--;
		// And swap it with the current element.
		[array[currentIndex], array[randomIndex]] = [array[randomIndex], array[currentIndex]];
		}

	return array;
}

document.addEventListener('keydown', (event) => {
  var name = event.key;
  var code = event.code;

	//w up
  if (name === keys[0] && xChange==0){
      yChange=0
      xChange=-1
  }
  //s down
  if (name === keys[2] && xChange==0){
      yChange=0
      xChange=1
  }
	//d right
  if (name === keys[3] && yChange==0){
      yChange=1
      xChange=0
  }
  //a left
  if (name === keys[1] && yChange==0){
      yChange=-1
      xChange=0
  }

}, false);
//?? This prevents form resubmission
if ( window.history.replaceState ) {
        window.history.replaceState( null, null, window.location.href );
    }

var up = document.getElementById("up");
var down = document.getElementById("down");
var left = document.getElementById("left");
var right = document.getElementById("right");


var scoreMessage = document.getElementById("score");
var startButton = document.getElementById("start");
startButton.addEventListener( "click", drawSnake);
