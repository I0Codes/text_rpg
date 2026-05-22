Enemy art drop-in folder
========================

The Kivy combat screen looks up images by lowercased enemy name:

    goblin.png   bandit.png   wolf.png
    orc.png      troll.png    dragon.png
    skull.png    <- used as the "defeated" portrait

Drop PNGs (or .jpg / .jpeg) into this folder using exactly those filenames
and they will be picked up automatically the next time combat starts.

If no PNG is present for an enemy, the screen falls back to a coloured
placeholder with a Unicode glyph (👺🐺🗡👹🧌🐲). The "defeated" state
falls back to 💀 when skull.png is missing.

Recommended portrait size: 512×512 (square) or 512×768 (tall). Larger is
fine — the widget scales the image while keeping aspect ratio.
