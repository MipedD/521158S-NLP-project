#include "task5widget.h"

#include <QLabel>
#include <QScrollArea>

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
    args << "-o" << QUrl::fromLocalFile(m_datasetDir.path() + "\\plot2.png").toLocalFile();

    connect(m_runner, &PythonScriptRunner::completed, this, &Task5Widget::displayGraph);
    m_runner->runPythonScript(m_scriptsDir.path() + "\\find_common_sentiments.py", args);
}

void Task5Widget::displayGraph()
{
    disconnect(m_runner, &PythonScriptRunner::completed, this, &Task5Widget::displayGraph);
    QScrollArea *area = new QScrollArea();
    area->setWindowTitle("Histogram of average categories for positive and negative reviews");
    area->setWindowFlag(Qt::Window, true);
    area->setAttribute(Qt::WidgetAttribute::WA_DeleteOnClose, true);
    QLabel *plot = new QLabel(area);
    plot->setPixmap(QPixmap(QUrl::fromLocalFile(m_datasetDir.path() + "\\plot2.png").toLocalFile()));
    area->setWidget(plot);
    area->show();
}
