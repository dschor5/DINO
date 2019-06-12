from threading     import Thread # Thread to record continuously
from threading     import RLock  # Note re-entrant lock
from threading     import Event  # Events for communicating within threads
import time
from DinoConstants import *
from DinoTime      import *
from DinoLog       import *
import sys
import csv
sys.path.append("../../DinoLambda/wrappers/python")
from threading     import Thread # Thread to record continuously
from threading     import RLock  # Note re-entrant lock
from threading     import Event  # Events for communicating within threads

from wrapper_python3 import *
from wrapper_python3.core import *
from wrapper_python3.device import *
from wrapper_python3.color import *


try:
   pass   
except:
   print(COLORS['TEST_FAIL'] + "ERROR" + COLORS['NORMAL'] + " - Spectrometer interface not loaded.")
class DinoSpectrometer(object):
   __instance = None
   # Constants for validating period between captures.
   MIN_PERIOD = 5.0
   MAX_PERIOD = SPECTROMETER_CAPTURE_INTERVAL
   """ Singleton instance. """
   connectReturn = 0;
   fileName = ""
   def __new__(self):
      #print"Create the Spectrometer Object")
      if(DinoSpectrometer.__instance is None):
         DinoSpectrometer.__instance = object.__new__(self)
         DinoSpectrometer.__isCapturing = False
         DinoSpectrometer.__servo       = None
         DinoSpectrometer.__thread      = None
         DinoSpectrometer.__lock        = None
         DinoSpectrometer.__stop        = None
         # Create lock object to protect shared resources
         # between the spectrometer object and the main thread.
         # Note that these are separate such that they reduce
         # deadlock scenarios:
          # Create lock object to protect shared resources.
         try:
            DinoSpectrometer.__lock = RLock()
         except:
            DinoLog.logMsg("ERROR - Could not create lock for the spectrometer thread.")

         # Create event to notify capturing thread when to stop.
         # While this could have been done with a lock, the event
         # has built in functions for checking if a flag is set.
         try:
            DinoSpectrometer.__stop = Event()
            DinoSpectrometer.__stop.set()
         except:
            DinoLog.logMsg("ERROR - Could not create event for Spectrometer.")
      return DinoSpectrometer.__instance


   def __del__(self):
      """
      Destructor that stops the active capturing and terminates the thread.
      """
      self.stopCapturing()

   def isCapturing(self):
      """
      Return True if thread is active and Spectrometer is capturing.
      """
      self.__lock.acquire()
      isCapturing = self.__isCapturing
      self.__lock.release()
      return isCapturing


   def startCapturing(self, period=MAX_PERIOD):
      """
       Start spectrum capture on the requested period.

      Parameters
      ----------
      period : float
         Time in seconds between spectrum captures.

      Returns
      -------
      bool
         True if it successfully started the spectrum capture.
         False if it was already running the thread.
      """
      # Ensure there is no capture is in progress.
      if(self.isCapturing() == True):
         return False

      # Validate input parameters

      if((period < self.MIN_PERIOD) or (period > self.MAX_PERIOD)):
         DinoLog.logMsg("ERROR - Invalid spectrometer period=[" + str(period) + "].")
         return False

      # Capture settings and start thread
      self.__period  = float(period)
      self.__stop.set()
    

      # Start thread.
      try:
         self.__stop.clear()
         self.__thread = Thread(target=self.__run, args=(self.__stop, self.__lock, self.__period,))
         self.__thread.start()
         status = (self.__thread is not None)
      except:
         DinoLog.logMsg("ERROR - Could not start Spectrometer thread.")
         status = False
      return status

   def stopCapturing(self):
      """
      Stop spectrometer capturing and terminate thread.
      Terminates the ongoing capture even if it has not finished
      the desired spectrum capture. This will also stop terminate
      continuous capture in order to end the thread.
      Return
      ------
      bool
         True if the capture was stopped or there was nothing running.
      """
      self.__stop.set()
      try:
         self.__thread.join()
         self.__thread = None
      except:
         return False
      return self.isCapturing()

   def initialize(object):
      print("initializing DinoSpectrometer......")
      initialize("/home/pi/DinoLambda/Libs/libCrystalBase_RPi.so")
      object.pSpecCore      = initialize_core_api("/home/pi/DinoLambda/Libs/libCrystalCore_RPi.so")
      object.pSpecDevice    = initialize_device_api("/home/pi/DinoLambda/Libs/libCrystalPort_RPi.so")
      initialize_color_api(object.pSpecCore)
      object.connectReturn   = connect_device(object.pSpecDevice)   # return total num of devices connected with system
   def captureSpectrum(object):
      if object.connectReturn > 0:

         (ret, sensorID) = get_sensor_id_device(object.pSpecDevice)
         create_core_object(object.pSpecCore)
         csInit_Return = load_sensor_file(object.pSpecCore, b"/home/pi/DinoLambda/config/sensor_" + sensorID + b".dat")
         if(csInit_Return > 0):
            (ret, sensorID) = get_sensor_id_file(object.pSpecCore)
            get_sensor_parameters_from_device(object.pSpecDevice)
            (adcGain,adcRange) = get_sensor_parameters_from_calibration_file(object.pSpecCore)
            settingReturn = set_sensor_parameters_to_device(object.pSpecDevice,adcGain,adcRange)
            total_num_of_sensors = total_sensors_connected(object.pSpecDevice)
            get_capacity_sensor_data_list(object.pSpecCore)
            for index in range(total_num_of_sensors):
            #activate a specific device(sensor)
               activatingReturn = index_activation(object.pSpecDevice,index)
               #get sensor id of currently activated device(sensor)
               (ret, sensorID) = get_sensor_id_device(object.pSpecDevice)
               #get and set shutter speed of device(sensor)
               get_shutter_speed(object.pSpecDevice)
               set_shutter_speed(object.pSpecDevice,1)
               #get one filter output (sensor data)
               filterData = get_filter_data(object.pSpecDevice,20)
               #set background data
               set_background_data(object.pSpecCore,filterData)
               #get and set shutter speed of device(sensor)
               #get_shutter_speed(object.pSpecDevice)
               valid_filters_num = get_num_of_valid_filters(object.pSpecCore)
               valid_filters = get_valid_filters(object.pSpecCore)
               newSS = 50
               frame_avg = 20
               do_AE = True
			      
	           #Get shutter speed with AE
               if do_AE:
                  newSS = get_optimal_shutter_speed(object.pSpecDevice,valid_filters_num,valid_filters)
               set_shutter_speed(object.pSpecDevice,newSS)
	           #convert shutter speed to exposure time (ms) for your reference
               ss_to_exposure_time(object.pSpecDevice,5,newSS)
      
               filterData = get_filter_data(object.pSpecDevice,frame_avg)
      
               specSize = get_spectrum_length(object.pSpecCore)
      
               (ret, specData,wavelengthdata) = calculate_spectrum(object.pSpecCore,filterData,newSS)
      
               (Start_Wavelength, End_Wavelength, Interval_Wavelength) = get_wavelength_information(object.pSpecCore)
      
               if sys.version_info[0] < 3:
                  fileName = (r"SpectromData2_" + sensorID + ".csv");
                  data = []
                  for i in range(get_spectrum_length(object.pSpecCore)):
                     data.append(str(specData[i]).split(","))
      
                  with open(fileName, "wb") as csv_file:
                     writer = csv.writer(csv_file, delimiter=',')
                     for line in data:
                      writer.writerow(line)
                  csv_file.close()
               else:
                  localtime = time.localtime(time.time())
                  completetime = str(localtime.tm_year) + \
                                 str(localtime.tm_mon) + \
                                 str(localtime.tm_mday) + \
                                 str(localtime.tm_hour) + \
                                 str(localtime.tm_min) + \
                                 str(localtime.tm_sec)            
                  fileName = (b"SpecrtumData3_" + sensorID + b".csv");
                  if(object.fileName == ""):
                   fileName = (completetime + ".csv")
                  else:
                   fileName =object.fileName
                  data = []
                  for i in range(get_spectrum_length(object.pSpecCore)):
                     data.append(str(specData[i]).split(","))
      
                  with open(fileName, 'w', newline='') as csvfile:
                     filewriter = csv.writer(csvfile, delimiter=',',
                     quotechar='|', quoting=csv.QUOTE_MINIMAL)
                     for line in data:
                        filewriter.writerow(line)
                  csvfile.close()
         else:
            print ("**********************************************************************")
            print ("[PrismError] Sensor Calibration File Not Present in Config Foler. Please copy Sensor Calibration File in Config file and execute again.")
            print ("**********************************************************************")
      else:
            print ("**********************************************************************")
            print ("[PrismError]Device Not Connected. Please connect Device and try again.")
            print ("**********************************************************************")
      close_color_api(object.pSpecCore)
      close_core_object(object.pSpecCore)
      disconnect_device(object.pSpecDevice)
      DinoLog.logMsg("Success - Captured Spectrum.")
      print("Captured Spectrum")
   def __run(self, stopEvent, lock, period):
      """
      Thread for Spectrometer.

      The thread runs once for a single capture (for testing) or
      continuosly for a stream of captures separated by a known period.
      If run continuosuly, the application must call stopCapture() to
      terminate the thread.

      Exit the loop if an error is encountered when commanding the spectrometer
      or when the stopEvent flag is set through the stopCapture() function.

      Parameter
      ---------
      stopEvent : threading.Event
         Flag to stop this thread from the main application.
         Set by calling the function stopCapture()
      lock : threading.RLock
         Re-entrant safe lock to edit self.__isCapturing variable.
         This is set when the thread starts and cleared when the thread ends.
         Used by the application to check whether the thread is started
         to capture the spectrum of light from the dinos on a regular schedule.
      period : float
         Time in seconds between spectrum captures.
      """
      # Set protected flag to show thread has started
      print("Capturing spectrum")

     # Set protected flag to show thread has started
      lock.acquire()
      self.__isCapturing = True
      lock.release()

      # Run main loop for a single or continuous mode.
      faultFound = False
      while((stopEvent.isSet() == False) and (faultFound == False)):

         try:
            self.initialize()
            self.captureSpectrum()
         except:
            DinoLog.logMsg("ERROR - Failed to capture spectrum.")
            faultFound = True
         # Wait until it is time to capture again.
         print("Sleep until period")
         time.sleep(period)
         print("Capture Period Expired")
      # Clear protected flag to show thread has started
      lock.acquire()
      self.__isCapturing = False
      lock.release()
      stopEvent.set()
      print("Stopping")

