const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const startButton = document.getElementById('start-button');
const stopButton = document.getElementById('stop-button');

let stream;
let recording = false;

startButton.addEventListener('click', () => {
  navigator.mediaDevices
    .getUserMedia({ video: true, audio: false })
    .then((mediaStream) => {
      stream = mediaStream;
      video.srcObject = mediaStream;
      video.play();
    })
    .catch((error) => {
      console.error('Error accessing webcam:', error);
    });
});

stopButton.addEventListener('click', () => {
  if (stream) {
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    stream.getTracks().forEach((track) => track.stop());
    recording = true;
  }
});
