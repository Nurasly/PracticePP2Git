# Mickey's Clock Application

A real-time Python digital-style clock built using `pygame`. The clock syncs with the local system time and uses graphic hands to display the minutes and seconds.

## Requirements
* Python 3.x
* Pygame (`pip install pygame`)

## Features
* **Right Hand:** Displays the current minutes.
* **Left Hand:** Displays the current seconds.
* **Real-time Sync:** Uses `datetime` to perfectly match system time.
* **Smart Rotation:** Utilizes `pygame.transform.rotate()` while preserving original image quality.

## How to Run
1. Ensure you have `mickey_hand.png` inside the `images/` directory. (Note: The image should be oriented pointing straight up at 12 o'clock).
2. Run the application from the root folder:
   ```bash
   python main.py