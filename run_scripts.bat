:: .bat file for in case GUI fails
@echo off

:: Task0 - The dataset is first processed to remove all unnecessary data to speed up the following steps
echo "Preparing data.."
python .\scripts\csv_parse.py -i .\data\Datafiniti_Hotel_Reviews.csv -o .\data\dataset_processed.csv -c 16,18

:: Task1 - In this task each review is going to be run through SentiStrength.
echo "TASK 1: Attempting to run sentistrength"
python .\scripts\parse_csv_for_sentistrength.py -i .\data\dataset_processed.csv -o .\data\temp.csv
java -jar .\scripts\thirdparty\sentistrengthclient\sentistrengthcom.jar sentidata .\scripts\thirdparty\sentistrengthclient\sentidata\ input .\data\temp.csv annotateCol 3 overwrite UTF8
python .\scripts\sentistrength_to_db.py -i .\data\temp.csv -o .\data\dataset_processed.csv

:: Task2 - During this step the dataset is going to be run through another sentiment analayzer - NLTK vader.
echo "TASK 2: Running VADER"
python .\scripts\vader_sentiment.py -i .\data\dataset_processed.csv -o .\data\dataset_processed.csv -c reviews.text

:: Task3 - In this task the Vader and SentiStrength results are going to be plotted in the same graph along with the actual reviews
echo "TASK 3: plotting user ratings vs sentiment analyzer output (plot in .\data\plot.png)"
python .\scripts\task3.py -i .\data\dataset_processed.csv -o .\data\plot.png

:: Task4 - This step is about finding lexical categories within each review
echo "TASK 4: running empathclient"
python .\scripts\empath_categories.py -i .\data\dataset_processed.csv -o .\data\temp.csv -c 2 -a
python .\scripts\find_empath_categories.py -i .\data\dataset_processed.csv -o .\data\empath_categories.txt -c 10

:: Task5
echo "TASK 5 & 6: Analyzing empathclient results"
python .\scripts\find_common_sentiments.py -s .\data\dataset_processed.csv -a 0 -p 3 -n 4 -v .\data\dataset_processed.csv -b 0 -c 9 -e .\data\dataset_processed.csv -i 0 -r 1 -g 10 -l .\data\empath_categories.txt

:: Task7 - In this task named entity recognition is performed on each individual review separately.
echo "TASK 7: running named entity tagger on reviews"
python .\scripts\find_named_entity_categories.py -i .\data\dataset_processed.csv -o .\data\dataset_named_entities.csv -c 2

:: Task8
echo "TASK 8: finding relation between named entity categories and sentiment polarity"
python .\scripts\task8.py -i .\data\dataset_named_entities.csv -r .\data\dataset_processed.csv -d 0 -f 1

:: Task9 - In this task the hypothesis that negative reviews entail argumentation will be tested.
echo "TASK 9: testing if negative reviews entail argumentation"
python .\scripts\task9.py -i .\data\dataset_processed.csv -e .\data\explanatory_wording.csv

:: Task10 - For task 10 each review is split into one of two classes: ambiguous or non-ambiguous
echo "TASK 10: ambiguous classes"
python .\scripts\ambiguous_class.py -i .\data\dataset_processed.csv -o .\data\dataset_processed.csv
echo "TASK 11: testing ambiguous classes in case of bad writing"
python .\scripts\unrecognized_words.py -i .\data\dataset_processed.csv -o .\data\recognized_words.csv

:: Task12 - In this task the goal was to test the following hypothesis: ambiguous reviews have bad readability
echo "TASK 12: testing ambiguous classes for bad readability"
python .\scripts\textstat_readability.py -i .\data\dataset_processed.csv -o .\data\dataset_processed.csv -c reviews.text
