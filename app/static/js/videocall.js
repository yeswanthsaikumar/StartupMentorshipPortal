use strict;

const localVideo = document.querySelector('video');

let localStream;

let localPeerConnection;

function gotLocalMediaStream(mediaStream){
  localStream = mediaStream;
  localVideo.srcobject = mediaStream;
}


function handleLocalMediaStreamError(error){
  console.log('navigator.getUserMedia error : ' ,error);
}


var configuration = { 
    "iceServers": [{ "url": "stun:stun.1.google.com:19302" }] 
};

const peerConnection = new RTCPeerConnection(configuration);

// Combine RTCPeerConnection with getUserMedia:
navigator.mediaDevices.getUserMedia({
  audio: true,
  video: true
})
.then(function(localStream) {
  localpeerConnection.addStream(localStream);
  localpeerConnection.createOffer()
  .then(sdp => peerConnection.setLocalDescription(sdp))
  .then(function() {
    console.log(peerConnection.localDescription);
  });
})
