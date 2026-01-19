import { startHandTracking } from "./handtrack.js";
import { isPinching } from "./gestures.js";
import { handleUI } from "./ui.js";

startHandTracking((hand, cursor) => {
  const pinching = isPinching(hand);
  handleUI(cursor, pinching);
});
