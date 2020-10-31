#include "task7widget.h"

Task7Widget::Task7Widget(QWidget *parent, const QString &taskName)
    : TaskWidget(parent, taskName)
{
    const QString description =
            "In this task named entity recognition is performed on each individual review separately. This is done "
            "again utilizing NLTK toolkit like described at <a href=\"https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da\">"
            "TowardsDataScience.com</a>.<br>"
            "For each review a binary vector is constructed which contains discovered named entities by categories. The vectors are stored in a separate "
            ".csv file (named_entities.csv)."

            "<br><br>"

            "<b>Please note</b>: running the script <b>will</b> take several minutes.";
    setDescription(description);
}

void Task7Widget::doExecuteTask()
{
    QStringList args;
    args << "-i";
    args << QUrl::fromLocalFile(m_datasetDir.path() + "\\dataset_processed.csv").toLocalFile();
    args << "-o";
    args << QUrl::fromLocalFile(m_datasetDir.path() + "\\dataset_named_entities.csv").toLocalFile();
    args << "-c";
    args << "2";
    m_runner->runPythonScript(m_scriptsDir.path() + "\\find_named_entity_categories.py", args);
}
