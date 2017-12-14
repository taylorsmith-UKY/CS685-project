# CS685-project
Parallel EEG pre-processing, feature extraction, and classification for automated sleep stage detection

This project provides all necessary programs to extract raw EEG data, perform all necessary pre-processing, and output feature vectors for overlapping, 30 second windows. Briefly:
  README.md                 -   This file
  ### Extract Signal Windows Into Text Files
  extract_windows.py        -   Python driver application to read raw EDF signal files and extract 30 second windows with a 50% overlap rate. Saves to CSV with 19 lines per window (i.e. 1 line per channel). Note that the output from this application is with the reference channel subtracted (so 20 total channels becomes 19). For example, each file should have a channel 'O1', as well as a channel 'A1', in which case the latter (the reference) is subtracted from the others. The output from this file has 19 `derived` channels, each with the same reference channel subtracted.
  extract_funcs.py          -   Functions definitions for window extraction.
  conf.json                 -   Configuration file for window extraction (notably input file names, window length, and overlap rate)
  
  ### Upload to HDFS
  commands.sh               -   Driver bash script to upload data to HDFS, perform all MR jobs, and save the final feature vectors locally
  to_hdfs.sh                -   Bash script that handles uploading the extracted text files to HDFS
  pp_mapper/reducer.py      -   Mapper and reducer to read windows from text files, apply a hamming window, perform a fourier transform to get the frequency space. For each window save the points for the feature vector on one line and statistics (max,min,mean,std) for the same vector on a second line.
  norm_stats_mapper/reducer.py  - Aggregate statistics output in previous step and save the same statistics for each channel across all patients (1 set of stats for each channel).
  save_norm_stats.py        -   Separate and save aggregate statistics to text file to pass to the next job.
  norm_mapper/reducer.py    -   Normalize each channel according to the statistics in the files saved by previous program. Due to the high amount of variability in FFT amplitudes, normalize to the range [mean - 2*std : mean + 2*std] for each channel.
  read_all_mapper.py        -   Most basic MR mapper possible. Simply return each line in each file in HDFS input directory.
  calc_entropy_reducer.py   -   Aggregate entropy statistics for each feature across all patients (feature = channel - freq. pair)
  pick_top_feats.py         -   Select the features with the highest entropy (number set at top of source file) and save to text file to pass to final MR job.
  feat_select_reducer.py    -   Read feature all feature vectors and select those matching the indices return from last step.
  
 Pre-requisites:
  Cloudera Quickstart VM - https://www.cloudera.com/downloads/quickstart_vms.html
    Python, Hadoop, MapReduce, Spark, PySpark, etc.
  NumPy (any version)
  
  Usage:
    1 - Update conf.json

    2 - Run extract_windows.py

        `python extract_windows.py`

    3 - Add files to to_hdfs.sh

    4 - Run commands.sh
          `./commands.sh`     (note, may need to run `sudo chmod +x commands.sh` first)

    5 - Features are saved locally... proceed as desired.
  
