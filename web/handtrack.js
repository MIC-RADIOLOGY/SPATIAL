export function startHandTracking(callback) {
  const video = document.getElementById("video");
  const canvas = document.getElementById("canvas");
  const ctx = canvas.getContext("2d");

  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  const hands = new Hands({
    locateFile: file =>
      `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`,
  });

  hands.setOptions({
    maxNumHands: 1,
    modelComplexity: 1,
    minDetectionConfidence: 0.7,
    minTrackingConfidence: 0.7,
  });

  hands.onResults(results => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (!results.multiHandLandmarks) return;

    const hand = results.multiHandLandmarks[0];
    const index = hand[8];

    const cursor = {
      x: index.x * canvas.width,
      y: index.y * canvas.height,
      z: index.z
    };

    // Draw cursor
    ctx.beginPath();
    ctx.arc(cursor.x, cursor.y, 10, 0, Math.PI * 2);
    ctx.fillStyle = "red";
    ctx.fill();

    callback(hand, cursor);
  });

  const camera = new Camera(video, {
    onFrame: async () => {
      await hands.send({ image: video });
    },
    width: 640,
    height: 480,
  });

  camera.start();
}
