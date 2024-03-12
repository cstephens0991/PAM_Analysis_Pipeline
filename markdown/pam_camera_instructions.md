---
title: "PAM Analysis Pipeline"
author: "Chris Stephens & Nick Dunken"
date: "2023-02-13"
---

## Imaging 24-well plates to generate .xpim files

_Described previously by Nick. See also "How to use the PAM camera.docx"_

![*Figure 1:* Layout of ImagingWin software. Note that the screenshot is taken in the "View only" setting, hence the options "New Record" and "Fo, Fm" being greyed out.](./screenshots/Screenshot_8.jpg)

1\. **Check the magnification of the PAM imaging camera**. This is located on the top of the PAM instrument. The magnification settings should be as shown in the image below. Note: this is *very important*, as an incorrect magnification can affect all downstream stages of the data analysis!

![*Figure 2:* Correct magnification settings for the PAM camera.](./screenshots/Screenshot_14.jpg)

1\. Place the 24-well plates to be imaged in the drawer under the PAM imager laptop (in the microscopy room, 4.302). Leave them in the dark for 15 minutes. There is a notice on the door to the microscopy room: "Plants in dark/PAM imaging". Post this on the outside of the door to notify others that you require the room to stay dark.

2\. After 15 minutes, turn on the power supply and light source to the PAM imager (units to the left of the laptop). The switch for the light source is on the back of the unit.

3\. Password for the computer is "12345". Open ImagingWin software and select "MAXI" setting.

***Carry out following stages in the dark to keep plants dark-adapted***

4\. Lift the red shield around the imaging platform. Transfer the first 24-well plate from the drawer to the platform.
 
 - Note: *Place the plates flush against the barriers at the back and right side of the platform, to ensure uniform well positioning. This is very important for automated downstream analysis!*

5\. Lower the red shield before imaging the plate.

6\. On the ImagingWin GUI page, there is a large "Fo, Fm" button (see image above). Click on this to take image measurements.

7\. Above the "Fo, Fm" button, there are a series of options for image channels. Click on the "Fv/Fm" channel. The plants should be clearly highlighted against a black background.
 
 - If the plants are not clearly highlighted, they may not be fully dark-adapted. Return the plate to the drawer for at least 10 minutes, then repeat above steps.

8\. Left of the "Fo, Fm" button is a "save" icon. Click on that to save the output as a PIM file.
 
 - Save the file in your own folder within the Data_MAXI folder. Once saved, a comment file will open automatically. This can be closed without adding a comment.

9\. Click on "New Record" button, immediately above "Fo, Fm". Answer "no" to the prompt to save image data.

- Note: Selecting "New Record" will delete any unsaved data from the ImagingWin memory. Make sure you save the image as a PIM file before carrying out this stage.

10\. Repeat steps 4 to 9 for all plates.