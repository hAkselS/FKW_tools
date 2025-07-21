'''
File:   glider_analyze_dataset.py

Spec:   This program looks into one of the two whisper 3.0 directories
        and analyzes a subset of images from the previous descent / ascent. 
        This program will call audio_to_spectro.py on 60 one minute data chunks 
        evenly spaced out from the previous ascent / descent. This program will 
        omit data from analyzing data within 10 minutes of the start of end of
        any ascent / descent. 

Usage:  python3 audio_transform/glider_analyze_dive.py <input/directory> -o <output/directory>

Notes:  (If the glider is current descending, this program will
        look at the previous ascent). Often there will be 5 hours of descent / ascent
        audio data, due to power concerns, the Raspberry Pi 5 can only analyze 60 minutes 
        of this data, hence, there will be large amounts of data unalyzed from previous deployments. 
        To avoid analyzing data from several deployments back, the analyst logs
        hold a start and end time for each deployment, thus only audio files 
        within the time window of the previous ascent / descent are candidates for analysis. 
        Data taken near the surface is unusable due to wave sounds, hence this program 
        will not analyze data that is within 10 minutes from the start or end of the dive.

'''

import os 
import argparse 
import subprocess
import pandas 

###################################################################
# CONFIGURATION DEFAULTS
audio_to_spectro_path = "audio_transform/audio_to_spectro.py"       # This program is a wrapper for audio_to_spectro 
count = 60                                                          # 60 images is ~ 1 Watthour of energy. 
###################################################################

