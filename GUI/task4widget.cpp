#include "task4widget.h"

Task4Widget::Task4Widget(QWidget *parent, const QString &taskName)
    : TaskWidget(parent, taskName)
{

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
