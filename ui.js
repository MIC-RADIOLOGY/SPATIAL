const button = document.getElementById("airBtn");
let wasPinching = false;

export function handleUI(cursor, pinching) {
  const rect = button.getBoundingClientRect();

  const hovering =
    cursor.x > rect.left &&
    cursor.x < rect.right &&
    cursor.y > rect.top &&
    cursor.y < rect.bottom;

  // Pseudo-3D depth effect
  const scale = Math.max(0.8, 1.3 - Math.abs(cursor.z));
  button.style.transform = `scale(${scale})`;

  if (hovering) {
    button.style.background = "#00bfff";

    if (pinching && !wasPinching) {
      buttonClicked();
    }
  } else {
    button.style.background = "#1e90ff";
  }

  wasPinching = pinching;
}

function buttonClicked() {
  alert("Gesture Click Detected");
}
