#include "task5widget.h"

Task5Widget::Task5Widget(QWidget *parent, const QString &taskName)
    : TaskWidget(parent, taskName)
{

}

void Task5Widget::doExecuteTask()
{

    const QString dataset = QUrl::fromLocalFile(m_datasetDir.path() + "\\dataset_processed.csv").toLocalFile();

    QStringList args;
    args << "-s" << dataset;
    args << "-a" << QString::number(0);
    args << "-p" << QString::number(3);
    args << "-n" << QString::number(4);
    args << "-v" << dataset;
    args << "-b" << QString::number(0);
    args << "-c" << QString::number(9);
    args << "-e" << dataset;
    args << "-i" << QString::number(0);
    args << "-r" << QString::number(1);
    args << "-g" << QString::number(10);
    args << "-l" << QUrl::fromLocalFile(m_datasetDir.path() + "\\empath_categories.txt").toLocalFile();

    m_runner->runPythonScript(m_scriptsDir.path() + "\\find_common_sentiments.py", args);
}
