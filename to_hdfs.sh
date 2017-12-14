hadoop fs -mkdir cs685
hadoop fs -mkdir cs685/project
hadoop fs -mkdir cs685/project/files

echo Copying File 1
hadoop fs -copyFromLocal /media/sf_Virtual_Share/windows/01-02-0001_windows_lbl.csv cs685/project/files/01-02-0001_windows.csv
echo Copying File 2
hadoop fs -copyFromLocal /media/sf_Virtual_Share/windows/01-02-0002_windows_lbl.csv cs685/project/files/01-02-0002_windows.csv
echo Copying File 3
hadoop fs -copyFromLocal /media/sf_Virtual_Share/windows/01-02-0003_windows_lbl.csv cs685/project/files/01-02-0003_windows.csv
echo Copying File 4
hadoop fs -copyFromLocal /media/sf_Virtual_Share/windows/01-02-0004_windows_lbl.csv cs685/project/files/01-02-0004_windows.csv
#echo Copying File 5
#hadoop fs -copyFromLocal /media/sf_Virtual_Share/windows/01-02-0005_windows_lbl.csv cs685/project/files/01-02-0005_windows.csv
#echo Copying File 6
#hadoop fs -copyFromLocal /media/sf_Virtual_Share/windows/01-02-0006_windows_lbl.csv cs685/project/files/01-02-0006_windows.csv
#echo Copying File 7
#hadoop fs -copyFromLocal 01-02-0007_windows_lbl.csv cs685/project/files/01-02-0007_windows.csv
#echo Copying File 8
#hadoop fs -copyFromLocal 01-02-0008_windows.csv cs685/project/files/01-02-0008_windows.csv
#echo Copying File 9
#hadoop fs -copyFromLocal 01-02-0009_windows.csv cs685/project/files/01-02-0009_windows.csv
#echo Copying File 10
#hadoop fs -copyFromLocal 01-02-0010_windows.csv cs685/project/files/01-02-0010_windows.csv
#echo Copying File 11
#hadoop fs -copyFromLocal 01-02-0011_windows.csv cs685/project/files/01-02-0011_windows.csv
#echo Copying File 12
#hadoop fs -copyFromLocal 01-02-0012_windows.csv cs685/project/files/01-02-0012_windows.csv
#echo Copying File 13
#hadoop fs -copyFromLocal 01-02-0013_windows.csv cs685/project/files/01-02-0013_windows.csv
#echo Copying File 14
#hadoop fs -copyFromLocal 01-02-0014_windows.csv cs685/project/files/01-02-0014_windows.csv
#echo Copying File 15
#hadoop fs -copyFromLocal 01-02-0015_windows.csv cs685/project/files/01-02-0015_windows.csv
#echo Copying File 16
#hadoop fs -copyFromLocal 01-02-0016_windows.csv cs685/project/files/01-02-0016_windows.csv
#echo Copying File 17
#hadoop fs -copyFromLocal 01-02-0017_windows.csv cs685/project/files/01-02-0017_windows.csv
#echo Copying File 18
#hadoop fs -copyFromLocal 01-02-0018_windows.csv cs685/project/files/01-02-0018_windows.csv
#echo Copying File 19
#hadoop fs -copyFromLocal 01-02-0019_windows.csv cs685/project/files/01-02-0019_windows.csv
echo Done copying to HDFS
