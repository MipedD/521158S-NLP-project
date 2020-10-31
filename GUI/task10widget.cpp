#include "task10widget.h"

Task10Widget::Task10Widget(QWidget *parent, const QString &taskName)
    : TaskWidget(parent, taskName)
{

}

void Task10Widget::doExecuteTask()
{
    QStringList args;
    args << "-i";
    args << QUrl::fromLocalFile(m_datasetDir.path() + "\\dataset_processed.csv").toLocalFile();
    args << "-o";
    args << QUrl::fromLocalFile(m_datasetDir.path() + "\\dataset_processed.csv").toLocalFile();

    m_runner->runPythonScript(m_scriptsDir.path() + "\\ambiguous_class.py", args);
}
