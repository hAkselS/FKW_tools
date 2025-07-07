'''
File:   create_pamguard_annotatoins.py

Spec:   This program looks at the spectrograms you have already made and assigns each one a datetime range.
        This program then looks at existing pamguard annotations and determines if
        any PAMGuard annotations fall within a time range of an existing spectrogram. If an annotation falls
        within the time range of a spectrogram, a new annotation (compatible with the FKW_tool spectrogram format) is created and saved as a text file. 

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
import sys

###################################################################
# CONFIGURATION DEFAULTS
desired_species = 33 # False Killer Whale (not used currently)
cruise_numbers = [1705, 1706] # Lasker, Sette (not used currently)
file_and_datatime = [] # A list of spectrogram names versus their respective start time
matched_PAM_annotations = [] # A list of annotations who's time intersect with existing spectrograms
frequency_range = 5000 # The difference between the minimum and maximum frequencies shown in the spectrograms
top_of_spectrogram_freq = 9000 # The frequency at the very top of the spectrogram strip 
normalized_strip_height = 0.08394736909 # The vertical heigh of each strip (how thicc it is)
normalized_stripe_ys = {
    "y0": 0.00000000000000000,
    "y1": 0.10163253864469451,
    "y2": 0.20314887407501037,
    "y3": 0.3059226305752359,
    "y4": 0.4067793229338596,
    "y5": 0.5089243688991303,
    "y6": 0.6102942321889212,
    "y7": 0.712957875364088,
    "y8": 0.8144914649867669,
    "y9": 0.9160526309037224

} # Each number represents the normalized top of each strip
freq_to_norm_conversion_factor = normalized_strip_height / frequency_range # used to translate between a change in frequency to a change in norm
time_to_norm_conversion_factor = 1 / 3 # the full screen is 1 unit and represents 3 seconds of time
###################################################################

# Accept command line args
parser = argparse.ArgumentParser()
parser.add_argument("spectrogram_folder", help="this folder should contain the spectrograms you have already made.")
parser.add_argument("csv_filepath", help="this csv file should contain vocalization localizations.")
args = parser.parse_args()

# TODO: add a function to choose output location 

# Turn args into variables (style points)
spectrogram_folder = args.spectrogram_folder 
csv_filepath = args.csv_filepath

## HELPER FUNCTIONS 

# Translate JPG file names to python datetimes 
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
def find_spectro_times(path_to_spectros):
    ''''
    This function looks at the directory where spectrograms are stored
    and saves a list of spectrogram names versus the times which they represent.
    '''
    file_names = os.listdir(path_to_spectros)
    file_names = [f for f in file_names if os.path.isfile(os.path.join(path_to_spectros,f))]

    for i in file_names: 
        time = file_name_to_time(i)
        entry = [i, time]
        file_and_datatime.append(entry)

# Get annotations from PAMGuard csv output 
def load_original_annotations(path_to_annotations):
    '''
    This function compares times of existing spectrograms with annotation times.
    If an annotation time is within 30 seconds of a sepctrogram's time, key information
    about the annotation is appended to the matched_PAM_annotations list. 
    '''

    # Load CSV using pandas
    df = pd.read_csv(path_to_annotations)

    # Parse UTC column to datetime
    df['UTC'] = pd.to_datetime(df['UTC'], format='mixed') # Potential bug here, some strings do not have the fractional element # format='%Y-%m-%d %H:%M:%S.%f'
    # Loop through each row in the CSV
    for _, row in df.iterrows():
        annotation_time = row['UTC']

        for fname, spectro_time in file_and_datatime:
            time_diff = (annotation_time - spectro_time).total_seconds()
        
            if 0 <= time_diff <= 30:
                    # Match found — store selected fields
                    matched_PAM_annotations.append({
                        'spectro_file': fname,
                        'file_time': spectro_time,
                        'UTC': annotation_time,
                        'duration': row['duration'],
                        'freqMin': row['freqMin'],
                        'freqMax': row['freqMax'],
                        'species': row['species']
                    })
                    #  break  # Found a match, no need to keep checking other spectros (removed, i want to find multiple matches)

    if(len(matched_PAM_annotations) == 0):
        print("None of the provided spectrograms match with the provided annotations... Exiting")
        sys.exit(1)
    
    return matched_PAM_annotations

# Determine bounding box normalized x values and return strip numbers 
def find_box_xs(spectrogram_start_time, bbox_start_time, bbox_duration): 
    '''Find the difference between the spectrogram start time and bbox start time
    to determine the strip that the bbox starts in. Normalize the duration to return coordinates
    and also determine if the annotation occurs on multiple strips.
    '''
    left_over = 0 

    time_diff = (bbox_start_time - spectrogram_start_time).total_seconds()

    # Each strip is 3 seconds, find the remainder (modulo) then convert to normalized coordinates
    norm_start = ((time_diff % 3) - 1)* time_to_norm_conversion_factor # TODO: -1 IS ADDED BECAUSE I'M VISUALLY SEEING ANNOTATIONS ARE OFF TO THE RIGHT ON THE ACTUAL LOCATIONS
    # Normalize the duration then add to the normalized start time
    norm_stop = norm_start + (bbox_duration * time_to_norm_conversion_factor) 
    if norm_stop > 1: # In the case the the bbox extends beyond one strip
        left_over = norm_stop - 1 # How much of the bounding box continues onto the next row (normalized)
        norm_stop = 1

    # Determine what row the annotations lives in
    row_number = int(time_diff // 3) # 3 seconds per strip (0 - 9)
    
    return row_number, norm_start, norm_stop, left_over

# Determine bounding box normalized y values
def find_box_ys(freqHigh, freqLow, strip_number): 
    '''Receive a strip number (from another function) then use the frequency
    min and max to find the normalized min and max. Note: y=0.0 is the TOP of the image.
    y0 (the first strip) starts at 0.0 and grows down! Frequency is translate as the difference between 
    the 9k (the top of the strip) and target value.'''
    # Check for valid strip number (between 1 and 10)
    if not 0<=strip_number <= 9: 
        print("Invalid strip number! There are 10 strips number from 0 to 9... Existing")
        sys.exit(1) 
    
    norm_high = ((top_of_spectrogram_freq - freqHigh) * freq_to_norm_conversion_factor) + list(normalized_stripe_ys.values())[strip_number]
    norm_low = ((top_of_spectrogram_freq - freqLow) * freq_to_norm_conversion_factor) + list(normalized_stripe_ys.values())[strip_number]

    return norm_high, norm_low
    
def export_annotations(matched_PAM_annotations): 
    '''
    Turn each annotation into a text file in YOLO OBB format. 
    '''
    if not os.path.exists('annotations'):
        print("annotations directory does not exist, please create an 'annotations' directory in your project root.")
        return
    
    for ann in matched_PAM_annotations: # [:10] (if testing only the first ten)
        # Create file name based on associated .jpg file
        base_name = os.path.splitext(ann['spectro_file'])[0]
        text_file_name = f'annotations/{base_name}.txt'
        try:
            with open(text_file_name, 'a') as file:  # open in append mode
                class_index = ann['species']
                if class_index == 33:
                    class_index = '0'

                bbox_start_time = ann['UTC'] 
                bbox_duration = ann['duration']
                freq_high = ann['freqMax']
                freq_low = ann['freqMin']
                # FILE_NAME = ann['spectro_file'] # Stored for reference if needed
                file_start_time = ann['file_time']
                
                row_number, norm_start, norm_stop, left_over = find_box_xs(file_start_time, bbox_start_time, bbox_duration)
                norm_high, norm_low = find_box_ys(freq_high, freq_low, row_number)

                # Using the x1,y1 x2,y2 x3,y3 x 4,y4 format
                # line = f"{class_index} {norm_start} {norm_high} {norm_stop} {norm_high} {norm_start} {norm_low} {norm_stop} {norm_low}\n"
                
                # Using the x y width height format 
                width = norm_stop - norm_start
                height = norm_low - norm_high # y=0 is the TOP of the figure 
                middle_point_x = norm_start + (width/2)
                middle_point_y = norm_high + (height/2)
                
                line = f"{class_index} {middle_point_x} {middle_point_y} {width} {height}\n"

                file.write(line)
        except FileNotFoundError:
            print("annotations directory does not exist, please create an 'annotations' directory in your project root.")
            return

    print('finished dakine')


print("Creating YOLO OBB annotations from PAMGuard annotations. :)\n")

find_spectro_times(spectrogram_folder)

load_original_annotations(csv_filepath)

export_annotations(matched_PAM_annotations)