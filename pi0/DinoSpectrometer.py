
from DinoConstants import *
from DinoTime      import *
from DinoLog       import *
import sys
import csv
sys.path.append("../../DinoLambda/wrappers/python")
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
   """ Singleton instance. """
   connectReturn = 0;
   def __new__(self):
      #print"Create the Spectrometer Object")
      if(DinoSpectrometer.__instance is None):
         DinoSpectrometer.__instance = object.__new__(self)
      return DinoSpectrometer.__instance
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
                  fileName = (r"SpecrtumData2_" + sensorID + ".csv");
                  data = []
                  for i in range(get_spectrum_length(object.pSpecCore)):
                     data.append(str(specData[i]).split(","))
      
                  with open(fileName, "wb") as csv_file:
                     writer = csv.writer(csv_file, delimiter=',')
                     for line in data:
                      writer.writerow(line)
                  csv_file.close()
               else:
                  fileName = (b"SpecrtumData3_" + sensorID + b".csv");
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
      


