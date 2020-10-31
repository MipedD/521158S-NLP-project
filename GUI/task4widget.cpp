#include "task4widget.h"

Task4Widget::Task4Widget(QWidget *parent, const QString &taskName)
    : TaskWidget(parent, taskName)
{
    const QString description =
            "This step is about finding lexical categories within each review. <a href=https://github.com/Ejhfast/empath-client>Empath</a> "
            "is used for finding the categories and empath output will be saved to the database."

            "<br><br>"

            "<b>Please note</b>: running the script may take up to few minutes. The amount of data processed is significant.";
    setDescription(description);
}

void Task4Widget::doExecuteTask()
{
    QStringList args;
    args << "-i";
    args << QUrl::fromLocalFile(m_datasetDir.path() + "\\dataset_processed.csv").toLocalFile();
    args << "-o";
    args << QUrl::fromLocalFile(m_datasetDir.path() + "\\temp.csv").toLocalFile();
    args << "-c";
    args << "2";
    args << "-a";
    m_runner->runPythonScript(m_scriptsDir.path() + "\\empath_categories.py", args);
}
