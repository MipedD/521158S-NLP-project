:: .bat file for in case GUI fails
@echo off

:: Task0 - The dataset is first processed to remove all unnecessary data to speed up the following steps
python .\scripts\csv_parse.py -i .\data\Datafiniti_Hotel_Reviews.csv -o .\data\dataset_processed.csv -c 16,18

:: Task1 - In this task each review is going to be run through SentiStrength.
python .\scripts\parse_csv_for_sentistrength.py -i .\data\dataset_processed.csv -o .data\temp.csv
:: TODO - Run SentiStrength java client
python .\scripts\sentistrength_to_db.py -i .\data\temp.csv -o .data\dataset_processed.csv

:: Task2 - During this step the dataset is going to be run through another sentiment analayzer - NLTK vader.
python .\scripts\vader_sentiment.py -i .\data\dataset_processed.csv -o .\data\dataset_processed.csv

:: Task3 - In this task the Vader and SentiStrength results are going to be plotted in the same graph along with the actual reviews
python .\scripts\task3.py -i .\data\dataset_processed.csv -o .\data\plot.png

:: Task4 - This step is about finding lexical categories within each review
python .\scripts\empath_categories.py -i .\data\dataset_processed.csv -o .data\temp.csv -c 2 -a
python .\scripts\find_empath_categories.py -i .\data\dataset_processed.csv - o .data\empath_categories.txt -c 10

:: Task5
python .\scripts\find_common_sentiments.py -s .\data\dataset_processed.csv -a 0 -p 3 -n 4 -v .\data\dataset_processed.csv -b 0 -c 9 -e .\data\dataset_processed.csv -i 0 -r 1 -g 10 -l .data\empath_categories.txt

:: Task7 - In this task named entity recognition is performed on each individual review separately.
python .\scripts\find_named_entity_categories.py -i .\data\dataset_processed.csv -o .\data\dataset_named_entities.csv -c 2

:: Task8
python .\scripts\task8.py -i .data\\dataset_named_entities.csv -r .\data\dataset_processed.csv -d 0 -f 1

:: Task9 - In this task the hypothesis that negative reviews entail argumentation will be tested.
python .\scripts\task9.py -i .\data\dataset_processed.csv -e .\data\explanatory_wording.csv

:: Task10 - For task 10 each review is split into one of two classes: ambiguous or non-ambiguous
python .\scripts\ambiguous_class.py -i .\data\dataset_processed.csv -o .\data\dataset_processed.csv
python .\scripts\unrecognized_words.py -i .\data\dataset_processed.csv -o .\data\recognized_words.csv

:: Task12 - In this task the goal was to test the following hypothesis: ambiguous reviews have bad readability
python .\scripts\textstat_readability.py -i .\data\dataset_processed.csv -o .\data\dataset_processed.csv -c reviews.text
