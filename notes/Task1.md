# Sentistrength
## Java version
### How do we use it?

Running the java version is fairly simple. In the uploaded sentistrength output I have used mostly the default settings. I ran sentistrength with the following command:

1) java -jar path/to/SentiStrengthCom.jar sentidata path/to/sentidata/ input path/to/input_file annotateCol 3 overwrite
2) java -jar path/to/SentiStrengthCom.jar sentidata path/to/sentidata/ input path/to/input_file annotateCol 3 overwrite scale

#### notes
* the input is expected to be .csv but tab separated ('\t')
* the output is written directly into the input file
* sentistrength will analyze even the header (first row) so that has to be corrected manually (or ignored)
* this does NOT produce the overall sentiment - the second run is required for it 
