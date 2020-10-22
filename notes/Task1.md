# Sentistrength
## Java version
### How do we use it?

Running the java version is fairly simple. In the uploaded sentistrength output I have used mostly the default settings. I ran sentistrength with the following command:

java -jar path/to/SentiStrengthCom.jar sentidata path/to/sentidata/ input path/to/input_file annotateCol 3 overwrite

#### notes
* the input is expected to be .csv but tab separated ('\t')
* the output is written directly into the input file
* sentistrength will analyze even the header (first row) so that has to be corrected manually (or ignored)