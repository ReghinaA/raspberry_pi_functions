# raspberry_pi_functions
educational app that teaches kids python functions

<a href="https://ko-fi.com/birchtree1113">
  <img src="birchtree1113-Sharable-Profile)-Horizontal.jpg" width="200">
</a>

# Python Quest <img src="dinosaur.png" width="70">

Down the rabbit hole I went: I sat down to get familiar with Claude Code, and somehow ended up building an app for Raspberry Pi. The code was generated with Claude's help.

Python Quest is a small, interactive app that teaches kids the basics of Python through a friendly, touchscreen-style interface. It's built with [Pygame](https://www.pygame.org/) and sized for a Raspberry Pi touchscreen (1024×600), though it runs fine on a regular desktop too.

## Features

- **Welcome screen** with a short introduction and a dinosaur mascot.
- **Lesson 1 — Functions**: explains what a function is, then lets kids click buttons to see real function code side-by-side with plain-English explanations, and run the code to see the result.
- **Guess the Output**: a quiz where kids read a short snippet of Python and pick what they think it will print, with instant right/wrong feedback.

## Credits

Developed by BirchTree

Dinosaur image credit — ArtsyBeeKids

## Display compatibility

Python Quest automatically adapts to whatever screen it's running on. Instead of assuming a fixed screen size, the app draws everything on a small internal canvas first, then scales that canvas up (or down) to fit the real screen — as large as possible while keeping everything in the correct proportions, so nothing looks stretched or squashed.

Works on any resolution. Whether it's a small 7" touchscreen, a laptop display, or a larger monitor, the app detects the actual screen size at startup and fits itself to it automatically — no configuration needed.
No distortion. If the screen's proportions don't exactly match the app's design, you'll see a thin plain-colored margin on the sides (or top/bottom) instead of a stretched, blurry picture.
Fullscreen or windowed. The app can run fullscreen (recommended for a dedicated device like a Raspberry Pi kiosk) or in a regular resizable window (handy for testing on a laptop).

## Requirements

- Python 3
- [Pygame](https://www.pygame.org/) (tested with 2.6.1)

Install the dependency with:

```bash
pip install pygame
