#include "task0widget.h"

Task0Widget::Task0Widget(QWidget *parent, const QString &taskName)
    : TaskWidget(parent, taskName)
{
    const QString description =
            "The dataset is first processed to remove all unnecessary data to speed up the following steps. "
            "In practice all but the most essential (reviews.text, reviews.rating) columns are removed from the dataset. "
            "Additionally a new column ID is added which holds a unique key for each review.";
    setDescription(description);
}

void Task0Widget::doExecuteTask()
{
    QStringList args;
    args << "-i";
    args << QUrl::fromLocalFile(m_datasetDir.path() + "\\Datafiniti_Hotel_Reviews.csv").toLocalFile();
    args << "-o";
    args << QUrl::fromLocalFile(m_datasetDir.path() + "\\dataset_processed.csv").toLocalFile();
    args << "-c";
    args << "16,18";
    m_runner->runPythonScript(m_scriptsDir.path() + "\\csv_parse.py", args);
}
