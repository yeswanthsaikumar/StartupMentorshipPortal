'use strick';

var contraints = {

	video : true , audio : true
}

function successCallback(stream){
	var video = document.querySelector('video');
	video.srcObject = stream;
}

function errorCallback(error){
	console.log( " navigator.getUserMedia error", error);
}


navigator.getUserMedia( contraints, successCallback , errorCallback);

