#include "task6widget.h"

Task6Widget::Task6Widget(QWidget *parent, const QString &taskName)
    : TaskWidget(parent, taskName)
{

}

void Task6Widget::doExecuteTask()
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
