def __init__(self, resolution=(320, 240), framerate=32, shutterspeed=1000):
		# initialize the camera and stream
		self.camera = PiCamera()
		self.camera.resolution = resolution
		self.camera.framerate = framerate
    self.camera.shutter_speed=shutterspeed
		self.rawCapture = PiRGBArray(self.camera, size=resolution)
		self.stream = self.camera.capture_continuous(self.rawCapture,
			format="bgr", use_video_port=True)

		# initialize the frame and the variable used to indicate
		# if the thread should be stopped
		self.frame = None
		self.stopped = False
 #USE THIS AS THE INIT BLOCK FOR PiVideoStream for our code
