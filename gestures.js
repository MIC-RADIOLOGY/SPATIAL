export function isPinching(hand) {
  const thumb = hand[4];
  const index = hand[8];

  const dx = thumb.x - index.x;
  const dy = thumb.y - index.y;

  const distance = Math.sqrt(dx * dx + dy * dy);
  return distance < 0.03;
}
