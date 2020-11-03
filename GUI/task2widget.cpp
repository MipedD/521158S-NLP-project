#include "task2widget.h"

Task2Widget::Task2Widget(QWidget *parent, const QString &taskName)
    :TaskWidget(parent, taskName)
{
    const QString description =
            "During this step the dataset is going to be run through another sentiment analayzer - NLTK vader. "
            "The process here is almost identical to what was done in the previous step except results will be written"
            " directly to the database file.";
    setDescription(description);

    QStringList requirements;
    requirements << "Preparation step completed";
    requirements << "nltk vader installed";
    setRequirements(requirements);
}

void Task2Widget::doExecuteTask()
{
    QStringList args;
    args << "-i";
    args << QUrl::fromLocalFile(m_datasetDir.path() + "\\dataset_processed.csv").toLocalFile();
    args << "-o";
    args << QUrl::fromLocalFile(m_datasetDir.path() + "\\dataset_processed.csv").toLocalFile();
    args << "-c";
    args << "reviews.text";
    m_runner->runPythonScript(m_scriptsDir.path() + "\\vader_sentiment.py", args);
}
