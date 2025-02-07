#!/usr/bin/python

'''
  bci_tinder.py
  ---------------
  UCLA Crux UCLA - Team 12
  Author - Abril Aguilar Lopez
  ---------------
  This is the main program for the BCI tinder app
  This include the implementation of opening and reading from the LSL stream 
  for real time data streaming from the board to the program,
  and writing the samples to a local file
  for real time data streaming from the board to the program

  To run: `python bci_tinder.py <trial_name>`. 
  For more information, see Github:
  https://github.com/abril-AL/Crux
'''

import sys
import os
from datetime import datetime
import numpy as np # pip install numpy
import pandas as pd # pip install pandas
#import neurokit2 as nk # pip install neurokit2 ( from cmd administator )
# pip install mne ( as cmd admin )
# python -m pip install brainflow


def main(argv):
   if not argv:
      print( 'Please provide a valid trial ID argument')
      sys.exit()
   else:
      now = datetime.now()
      todayDate = now.strftime("-%H-%M-%S")
      print("Trial ID: " + str(argv[0]) + "\n Time: " + str(todayDate))
      #after stream is resolved we now have timestamped samples
      # store in output file with unique name based on trial ID
      #will save fft , bandpass , and time series data
      
      store_fft = "fft" + str(argv[0])
      store_bandpass = "bandpass" + str(argv[0])
      store_time_series = "timeseries" + str(argv[0])

      # create the directory with the specified name, if it doesn't exist
      directory_name = str(argv[0])
      print(directory_name)
      os.mkdir(directory_name) #if not os.path.exists(directory_name):
          
      # open the files in the directory
      fft = open(store_fft ,"x")
      bp = open(store_bandpass, "x")
      ts = open( store_time_series, "x")

      """Read a multi-channel time series from LSL."""
      from pylsl import StreamInlet, resolve_stream, resolve_byprop

      # first resolve an EEG stream by prop for each type
      print("looking for an EEG stream...")
      streams_FFT = resolve_byprop("name", "fft")
      streams_BP = resolve_byprop("name", "bandpass")
      streams_TS = resolve_byprop("name", "timeseries")
      print("all streams connected")
      # create a new inlet to read from the named streams
      inlet_FFT = StreamInlet(streams_FFT[0])
      inlet_BP = StreamInlet(streams_BP[0])
      inlet_TS = StreamInlet(streams_TS[0])
      
      '''TODO
      while True has issues with pulling from inlet
      need to read from full lsl , not just while the program runs or LSL is streaming
      samples no. not aligned
      need to pull samples after end of trial
      '''
      while True:
         sample_fft, timestamp_fft = inlet_FFT.pull_sample()
         sample_bp, timestamp_bp = inlet_BP.pull_sample()
         sample_ts, timestamp_ts = inlet_TS.pull_sample()
         #print(timestamp_fft, sample_fft)
         #print(timestamp_bp, sample_bp)
         #print(timestamp_ts, sample_ts)
         fft.write(str(sample_fft))
         fft.write('\n')
         #note that bp will have some arrays of 0 ( time reason i think )
         bp.write(str(sample_bp))
         bp.write('\n')
         ts.write(str(sample_ts))
         ts.write('\n')

if __name__ == '__main__':
   main(sys.argv[1:])
   # only argument is that of the name of the trial 
