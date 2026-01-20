import streamlit as st

st.set_page_config(page_title="Gesture UI", layout="wide")
st.title("🖐️ Gesture Controlled Spatial UI")

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <style>
    body {
      margin: 0;
      overflow: hidden;
      background: #0e0e0e;
      font-family: Arial, sans-serif;
    }

    video {
      display: none;
    }

    canvas {
      position: absolute;
      top: 0;
      left: 0;
    }

    #airBtn {
      position: absolute;
      top: 35%;
      left: 35%;
      padding: 40px 60px;
      font-size: 24px;
      border-radius: 12px;
      border: none;
      background: #1e90ff;
      color: white;
      cursor: pointer;
      transition: transform 0.1s, background 0.1s;
    }

    #status {
      position: fixed;
      bottom: 10px;
      left: 10px;
      color: white;
      font-size: 14px;
      background: rgba(0,0,0,0.5);
      padding: 8px 12px;
      border-radius: 6px;
    }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js"></script>
</head>

<body>
  <video id="video" autoplay playsinline></video>
  <canvas id="canvas"></canvas>
  <button id="airBtn">AIR BUTTON</button>
  <div id="status">Waiting for hand…</div>

  <script type="module">
    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");
    const button = document.getElementById("airBtn");
    const status = document.getElementById("status");

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    window.addEventListener("resize", () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    });

    let lastPinch = false;

    function isPinching(hand) {
      const thumb = hand[4];
      const index = hand[8];
      const dx = thumb.x - index.x;
      const dy = thumb.y - index.y;
      const dz = thumb.z - index.z;
      const distance = Math.sqrt(dx*dx + dy*dy + dz*dz);
      return distance < 0.06;
    }

    const hands = new Hands({
      locateFile: (file) =>
        `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`,
    });

    hands.setOptions({
      maxNumHands: 1,
      modelComplexity: 1,
      minDetectionConfidence: 0.6,
      minTrackingConfidence: 0.6,
    });

    hands.onResults((results) => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      if (!results.multiHandLandmarks) {
        status.textContent = "No hand detected";
        return;
      }

      status.textContent = "Hand detected";

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

      const pinching = isPinching(hand);

      if (pinching) {
        ctx.strokeStyle = "yellow";
        ctx.lineWidth = 3;
        ctx.stroke();
        status.textContent = "Pinching";
      }

      const rect = button.getBoundingClientRect();
      const hovering =
        cursor.x > rect.left &&
        cursor.x < rect.right &&
        cursor.y > rect.top &&
        cursor.y < rect.bottom;

      if (hovering) {
        button.style.background = "#00bfff";

        if (pinching && !lastPinch) {
          alert("Gesture Click Detected");
        }
      } else {
        button.style.background = "#1e90ff";
      }

      lastPinch = pinching;
    });

    const camera = new Camera(video, {
      onFrame: async () => {
        await hands.send({ image: video });
      },
      width: 640,
      height: 480,
    });

    camera.start();
  </script>
</body>
</html>
"""

st.components.v1.html(html_content, height=900, scrolling=False)
