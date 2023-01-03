Autonomous bot based on Vietnamese theme for ABU Robocon 2018: https://youtu.be/GAjVA2u-_1s.

Bot used a Camera (PS3 Eye) and OpenCV to detect the line.
Camera was connected to laptop. Laptop did all the heavy task of Image Processing and Data extraction. Once we get the info about line and position of robot then these values were passed to Nanpy whose task was to send those values from python code to Arduino Uno attach to that Laptop. Then this Uno was connected to our main Controller board which was an Arduino Mega with I2C.

**Camera Input:**

The camera we used is PS3 Eye since it provides a frame rate as high as 150 fps, which made it ideal for our use in the AR bot for the purpose of line tracing.
The source code for extracting and processing the feed obtained from the camera is written in Python.
The source code is primarily divided into three files in order to make it modular, hence improving its readability, and making it easier to maintain and debug it.

The three files are: -

1) **Credits.py**
  This file contains all the constants that we will be dealing with in the entire source code such as the resolution of the camera input. Hence it is aptly named ‘Credits’.

2) **Master.py**
  This file contains the source code where relevant data is extracted and processed from the camera and sent to the Arduino Mega.
  Initially, we make use of the video4linux application’s command line tools to disable the automatic white balance and auto exposure settings, and to set our own suitable parameters manually.
  This was necessary as it was observed that change in exposure interfered with our filters and generated noise.

  The OpenCV built-in functions that we’ve used are as follows: -

  cv2.videoCapture(cameraIndex)
  Returns a video capture object.

  VideoCaptureObject.set()
  Allows us to set, among other things, the resolution and frame rate of the video stream.

  VideoCaptureObject.read()
  Returns a Boolean variable along with an individual frame of the video stream.

  cv2.cvtcolor()
  Allows us to convert frame which is initially in BGR format into the HSV format. This is because the line that we wish to trace is white in color. And HSV format makes it easier to extract any single color from the screen.

  cv2.inRange()
  Used to define the range of the mask that will be applied later on the frame.

  cv2.bitwise_and()
  Used to apply the mask on the frame, thereby extracting a custom range of white from the frame.

  cv2.morphologyEx()
  This function is used to apply the two morphological transformations of opening and closing.
  Opening helps in removing any residual noise outside the principal object i.e. the line in our case.
  Closing helps in plugging any holes inside the line.

  cv2.imshow(windowname,image_name)
  Used to display the image on the screen. This is useful for checking if any form of noise is still present in our image. It proves extremely helpful in debugging and also calibration.

  cv2.waitkey(timeinterval)
  Displays the image for specified number of seconds

  cv2.destroyAllWindows()
  Closes all and any image windows.


  Numpy built-in functions used: -

  np.array()
  Used to define the lower and upper range of white that is to be extracted from the frame.

  np.ones()
  Used to set the kernel size which is needed to perform the morphological operations of opening and closing.

  User defined functions used: -

  fpsCount()
  Gives us the number of frames generated in one second. Used to monitor the effect of applying filters to the frames on the frame rate. The frame rate on the primary laptop was observed to be 35-45 fps while the same for the backup laptop was 40-50 fps

3) **Camera.py**

  Contains functions which are used to determine the position of line and also to detect a plus.

  The functions are as follows: -

  scan_up(image_name)
  Scans all the columns on a row at the top twice; once from the left and once from the right for maximum intensity and returns the average of the two values. This gives us the position of the line on the top.

  scan_down(image_name)
  Scans all the columns on a row at the bottom twice; once from the left and once from the right for maximum intensity and returns the average of the two values. This gives us the position of the line on the bottom.

  scan_left(image_name)
  Scans all the rows on a column on the left twice; once from the top and once from the bottom for maximum intensity and returns the average of the two values. This gives us the position of the line on the left.

  scan_right(image_name)
  Scans all the rows on a column on the right twice; once from the top and once from the bottom for maximum intensity and returns the average of the two values. This gives us the position of the line on the right.

  plus(thresh_name)
  Used to check for a cross, which helps in recording the position of the bot.
  If all the above four functions return non-zero values, it returns 1 indicating that a cross has been detected or else it returns 0.

