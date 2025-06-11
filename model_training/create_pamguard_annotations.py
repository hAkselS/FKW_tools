'''
File:   create_pamguard_annotatoins.py

Spec:   This program looks at the spectrograms you have already made and assigns each one a datetime range.
        This program then looks at existing pamguard annotations and determines if
        the annotation falls within a time range of an existing spectrogram. If an annotation falls
        within the time range of a spectrogram, a new annotation is created and saved as a text file. 

I/O:    This program expects a CSV with the following category names: 
            "","UID","UTC","freqBeg","freqEnd","freqMean","freqStdDev","duration","freqSlopeMean","freqAbsSlopeMean","freqPosSlopeMean","freqNegSlopeMean","freqSlopeRatio","freqStepUp","freqStepDown","numSweepsDwnFlat","numSweepsDwnUp","numSweepsFlatDwn","numSweepsFlatUp","numSweepsUpDwn","numSweepsUpFlat","numInflections","freqCofm","freqQuarter1","freqQuarter2","freqQuarter3","freqSpread","freqMin","freqMax","freqRange","freqMedian","freqCenter","freqRelBw","freqMaxMinRatio","freqBegEndRatio","freqNumSteps","stepDur","freqBegSweep","freqBegUp","freqBegDwn","freqEndSweep","freqEndUp","freqEndDwn","freqSweepUpPercent","freqSweepDwnPercent","freqSweepFlatPercent","inflMaxDelta","inflMinDelta","inflMaxMinDelta","inflMeanDelta","inflStdDevDelta","inflMedianDelta","inflDur","BinaryFile","eventId","detectorName","db","species"
        The aforementioned CSV should be a fairly straight forward product created
        via exporting cruise data from R. 

Note:   The last three digits is the AC number. Ex: 1705109 is LaskerAC109
Usage:  python3 model_training/create_pamguard_annotations.py <folder/with/spectrograms> <path/to/csv>
'''

import pandas as pd 
import argparse
from datetime import datetime, timedelta
import os


###################################################################
# CONFIGURATION DEFAULTS
desired_species = 33 # False Killer Whale 
cruise_numbers = [1705, 1706] # Lasker, Sette 
###################################################################

# Accept command line args
parser = argparse.ArgumentParser()
parser.add_argument("spectrogram_folder", help="this folder should contain the spectrograms you have already made.")
parser.add_argument("csv_filepath", help="this csv file should contain vocalization localizations.")
args = parser.parse_args()

# Turn args into variables (style points)
spectrogram_folder = args.spectrogram_folder 
csv_filepath = args.csv_filepath

## HELPER FUNCTIONS 
# Translate file names to times 
def file_name_to_time(file_name):
    # Remove prefix and suffix
    base = file_name.split('-')[0]  # '1706_20170709_034442_942'
    parts = base.split('_')  # ['1706', '20170709', '034442', '942']
    
    date_part = parts[1]  # '20170709'
    time_part = parts[2]  # '034442'

    # Combine into datetime object
    dt = datetime.strptime(f"{date_part}_{time_part}", "%Y%m%d_%H%M%S")

    # Check if '-0011' is in the filename and add 30 seconds if so
    if '-0011' in file_name:
        dt += timedelta(seconds=30)

    return dt


# Get datetimes from existing spectrograms
file_and_datatime = []
def find_spectro_times(path_to_spectros):
    ''''tbd'''
    file_names = os.listdir(path_to_spectros)
    file_names = [f for f in file_names if os.path.isfile(os.path.join(path_to_spectros,f))]

    for i in file_names: 
        time = file_name_to_time(i)
        entry = [i, time]
        file_and_datatime.append(entry)


# Load CSV using pandas
df = pd.read_csv(args.csv_filepath)

find_spectro_times(spectrogram_folder)

print(file_and_datatime)