'''
File:   create_pamguard_annotatoins.py

Spec:   Use this script to translate pamguard annotations to annotations usable with YOLO. 

I/O:    This program expects a CSV with the following category names: 
            "","UID","UTC","freqBeg","freqEnd","freqMean","freqStdDev","duration","freqSlopeMean","freqAbsSlopeMean","freqPosSlopeMean","freqNegSlopeMean","freqSlopeRatio","freqStepUp","freqStepDown","numSweepsDwnFlat","numSweepsDwnUp","numSweepsFlatDwn","numSweepsFlatUp","numSweepsUpDwn","numSweepsUpFlat","numInflections","freqCofm","freqQuarter1","freqQuarter2","freqQuarter3","freqSpread","freqMin","freqMax","freqRange","freqMedian","freqCenter","freqRelBw","freqMaxMinRatio","freqBegEndRatio","freqNumSteps","stepDur","freqBegSweep","freqBegUp","freqBegDwn","freqEndSweep","freqEndUp","freqEndDwn","freqSweepUpPercent","freqSweepDwnPercent","freqSweepFlatPercent","inflMaxDelta","inflMinDelta","inflMaxMinDelta","inflMeanDelta","inflStdDevDelta","inflMedianDelta","inflDur","BinaryFile","eventId","detectorName","db","species"
        The aforementioned CSV should be a fairly straight forward product created
        via exporting cruise data from R. 

Note:   The last three digits is the AC number. Ex: 1705109 is LaskerAC109
Usage:  python3 model_training/create_pamguard_annotations.py ... 
'''

import pandas as pd 
import argparse

###################################################################
# CONFIGURATION DEFAULTS
desired_species = 33 # False Killer Whale 
cruise_numbers = [1705, 1706] # Lasker, Sette 
###################################################################

# Accept command line args
parser = argparse.ArgumentParser()
parser.add_argument("csv_file_path", help="this csv file should contain vocalization localizations.")
args = parser.parse_args()

# Helper Function
def utc_format_transformer(input_time):
    ''' 
    Take an input of the form: 2017-08-18 13:39:03.945 (as in csv)
    and transform to: 1706_20170715_220250_436 (how wave files are saved)
    '''
    date_part, time_part = input_time.split()
    date_formatted = date_part.replace("-", "")
    time_main, millis = time_part.split(".")
    time_formatted = time_main.replace(":", "")
    return f"{date_formatted}_{time_formatted}_{millis}"

# Load CSV using pandas
df = pd.read_csv(args.csv_file_path)

# Access second row's 'utc' column
if 'UTC' in df.columns and len(df) > 1:
    test1 = df.loc[4120, 'UTC']
    print(utc_format_transformer(test1))
else:
    print("Column 'utc' not found or insufficient rows.")


