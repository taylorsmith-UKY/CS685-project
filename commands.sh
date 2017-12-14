/media/sf_Virtual_Share/to_hdfs.sh

hadoop jar /usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.6.0-mr1-cdh5.12.0.jar -input cs685/project/files/ -output cs685/project/feats_raw/ -mapper pp_mapper.py -reducer pp_reducer.py -file pp_mapper.py -file pp_reducer.py

hadoop jar /usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.6.0-mr1-cdh5.12.0.jar -input cs685/project/feats_raw/ -output cs685/project/norm_stats/ -mapper norm_stats_mapper.py -reducer norm_stats_reducer.py -file norm_stats_mapper.py -file norm_stats_reducer.py

hadoop fs -copyToLocal cs685/project/norm_stats/part-00000 norm_stats.txt
python save_stat_files.py


hadoop jar /usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.6.0-mr1-cdh5.12.0.jar -input cs685/project/feats_raw/ -output cs685/project/feats_norm/ -mapper norm_mapper.py -reducer norm_reducer.py -file norm_mapper.py -file norm_reducer.py -file means.txt -file stds.txt

hadoop jar /usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.6.0-mr1-cdh5.12.0.jar -input cs685/project/feats_norm/ -output cs685/project/entropy/ -mapper read_all_mapper.py -reducer calc_entropy_reducer.py -file read_all_mapper.py -file calc_entropy_reducer.py
hadoop fs -copyToLocal cs685/project/entropy/part-00000 entropy.txt
python pick_top_feats.py


hadoop jar /usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.6.0-mr1-cdh5.12.0.jar -input cs685/project/feats_norm/ -output cs685/project/final_feats/ -mapper read_all_mapper.py -reducer feat_select_reducer.py -file read_all_mapper.py -file feat_select_reducer.py -file 50feats.txt
hadoop fs -copyToLocal cs685/project/final_feats/part-00000 final_feats.txt
