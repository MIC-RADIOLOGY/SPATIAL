import streamlit as st

st.set_page_config(page_title="Gesture UI", layout="wide")
st.title("🖐️ Gesture Controlled Spatial UI")

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Gesture Controlled Spatial UI</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <style>
    body { margin: 0; overflow: hidden; background: #0e0e0e; font-family: Arial; }
    video { display: none; }
    canvas { position: absolute; top: 0; left: 0; }
    #airBtn { position: absolute; top: 40%; left: 40%; padding: 20px 30px; font-size: 18px; border-radius: 10px; border: none; background: #1e90ff; color: white; cursor: pointer; }
    #log { position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(0,0,0,0.6); color: white; font-size: 12px; padding: 10px; max-height: 120px; overflow-y: auto; }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js"></script>
</head>

<body>
  <video id="video" autoplay playsinline></video>
  <canvas id="canvas"></canvas>
  <button id="airBtn">AIR BUTTON</button>
  <div id="log"></div>

  <script type="module">
    const log = (msg) => {
      const logEl = document.getElementById("log");
      logEl.innerHTML += msg + "<br>";
      logEl.scrollTop = logEl.scrollHeight;
      console.log(msg);
    };

    log("Loading...");

    function isPinching(hand) {
      const thumb = hand[4];
      const index = hand[8];
      const dx = thumb.x - index.x;
      const dy = thumb.y - index.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      return distance < 0.03;
    }

    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    window.addEventListener("resize", () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    });

    const hands = new Hands({
      locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`
    });

    hands.setOptions({
      maxNumHands: 1,
      modelComplexity: 1,
      minDetectionConfidence: 0.7,
      minTrackingConfidence: 0.7,
    });

    hands.onResults((results) => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      if (!results.multiHandLandmarks || results.multiHandLandmarks.length === 0) {
        log("No hand detected");
        return;
      }

      const hand = results.multiHandLandmarks[0];
      const index = hand[8];

      const cursor = {
        x: index.x * canvas.width,
        y: index.y * canvas.height,
        z: index.z
      };

      ctx.beginPath();
      ctx.arc(cursor.x, cursor.y, 10, 0, Math.PI * 2);
      ctx.fillStyle = "red";
      ctx.fill();

      const pinching = isPinching(hand);

      const button = document.getElementById("airBtn");
      const rect = button.getBoundingClientRect();
      const hovering =
        cursor.x > rect.left &&
        cursor.x < rect.right &&
        cursor.y > rect.top &&
        cursor.y < rect.bottom;

      if (hovering) {
        button.style.background = "#00bfff";
        if (pinching) {
          log("PINCH DETECTED ON BUTTON");
        }
      } else {
        button.style.background = "#1e90ff";
      }
    });

    const camera = new Camera(video, {
      onFrame: async () => {
        await hands.send({ image: video });
      },
      width: 640,
      height: 480,
    });

    camera.start();

    log("Camera started. Waiting for hand...");
  </script>
</body>
</html>
"""

st.components.v1.html(html_content, height=900, scrolling=False)
