#include "task8widget.h"

Task8Widget::Task8Widget(QWidget *parent, const QString &taskName)
    : TaskWidget(parent, taskName)
{

}

void Task8Widget::doExecuteTask()
{
    QStringList args;
    args << "-i";
    args << QUrl::fromLocalFile(m_datasetDir.path() + "\\dataset_named_entities.csv").toLocalFile();
    args << "-r";
    args << QUrl::fromLocalFile(m_datasetDir.path() + "\\dataset_processed.csv").toLocalFile();
    args << "-d" << QString::number(0);
    args << "-f" << QString::number(1);

    m_runner->runPythonScript(m_scriptsDir.path() + "\\task8.py", args);
}
