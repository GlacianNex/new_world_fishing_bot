# **New World Fishing Bot**

## **DISCLAIMER**

>This program is meant to be used for purely educational purposes. Use of this program is a direct violation of Amazon Game Studio Terms of Service, and is a punishiable offence.

### **Requirements**

- Python - Verison 3.9
- New World runs in 1920 x 1080 resolution

### **Installation**

Navigate to root installation folder, and run the following command:
- `pip install -r requirements.txt`

>Note: It is possible that you will get installation / dependency errors. This guide will not cover on how to fix them, I encourage you to use Google / Stack Overflow to find the solution to your specific problems.

### **Running Bot**

1. Start New World, login to the character, go to a fishing location, and equip a fishing pole.

2. Turn off all quest, waypoint markers.
    > Being in an area with a lot of markers on your compas will interfear with bot functionality. Try to make sure that when you start the bot, there are no animal markers on your compass in front of you. 

3. To start the bot, naviator to root installation folder, and run '`run_bot.bat`' file.

4. Once the bot starts, you have five (5) seconds to go back to back to New World, and align your character in the direction you want bot to memorize.

5. Let the bot execute.

### **Notes**
- The bot will repair your fishing pole every hour.
- The bot will attempt to turn in the direction you were facing when the bot started fishing.
- The bot will **NOT** use any bait

### **How Bot Works & Design Decisions**

The bot works by capturing parts of the screen, looking for well known markers on the screen to determine game state and then take appropriate actions.

It uses `PILLOW` module to take screenshots, `numpy` to manipuate image matrix, and `opencv` to perform image matching.

Core bot loop can be found in `src/fishing_bot.py` file, with `src/game/screenshot_analyzer.py` responsible for image data analysis and `src/game/game_controller.py` responsible for contoling game inputs.

Before the start of fishing loop we first need to make sure we are facing the right way. To do that bot memorizes what did the center of your compas look like at the time it started.

Before it will try to start fishing it will then look at your compas and will try to make sure that it can find the same location, somewhere in +/- 20 degrees of center.

If it can't it will rotate to the right by 5 pixels, and try again until it is centered.

Fishing loop is fairly straight forward:

1. Wait till we can detect fishing menu with `change_bait_button.png`.
2. Press left mouse button and hold it for roughly 2 seconds.
3. Detect the position of the fishing indicator.
4. Check position of fishing indicator for `fish-on-hook.png` icon.
5. Once fish is on hook click left mouse button.
6. Go into reeling loop:
   - Locate reeling indicator with `reel-marker.png`
   - Extrapolate from location of reel marker, to capture the entire reel indicator.
   - Check if color of any pixel in reel indacator within the acceptable threshold. We do that by calcuating euclidian distance between the template green color, and each pixel color.
  
        > The color we compare it against is BGR(177, 235, 47). This is not a typo, we convert all images from RGB, to BGR format for correct color display.
   - If color is in the the accpetable threshold, hold down left mouse button. If not, let left mouse button go.
7. Check if we need to adjust compas facing.
8. Go back to the start of the loop.

### **Intresting Problems** ###

#### **Movement controls**

Since New World locks your mouse, use of `pydirectinput` library is somewhat messy. Specifically if you just use it as is, your screen will spin in crazy directions.

Through experimentation I found that if we move the screen slightly to start with, and go through a crazy spin, all following input gains a lot more stability. Given that we always want to make sure that our camera is looking down, we want to always drag Y input down. 

#### **Image Detection Speed**

Because fishing is a time gated activity, it is important that `opencv matchTemplate` function run fast enough for us to make a decision before it is too late.

To do that we agressively limit the area of the screen that we are working with. In general we are working with center top area of the screen, which is why the bot skews the screen down.

As an example of fishing marker will move to the left, or right edges of the screen the bot will not be able to detect them.

### **Known Issues**

- Right now there is a bug in the game where when you are reeling in a fish, it will sometime get stuck at 0.0m locations. The only way to fix is to right click the mouse.