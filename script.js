const { mouse, screen, ImageResource, straightTo, leftClick, waitFor } = require('@nut-tree/nut-js');
const { templateMatcher } = require('@nut-tree/template-matcher');

// Set image matcher
screen.config.matchMaker = templateMatcher;
screen.config.templateMatchSettings.confidence = 0.8; // Tune for accuracy

async function main() {
  // Load template (screenshot your target, e.g., 'attack.png')
  const targetImage = new ImageResource('attack.png');

  while (true) { // Loop forever or add exit condition
    try {
      // Find & click
      const location = await screen.find(targetImage);
      await mouse.move(straightTo(location));
      await leftClick();
      console.log('Clicked!');
    } catch (e) {
      console.log('Target not found, waiting...');
    }
    await new Promise(resolve => setTimeout(resolve, 100)); // 10 FPS poll
  }
}

main().catch(console.error);