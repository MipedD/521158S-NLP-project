#include "task1widget.h"

#include <QVBoxLayout>
#include <QTextEdit>
#include <QPushButton>

Task1Widget::Task1Widget(QWidget *parent, const QString &taskName)
    : TaskWidget(parent, taskName)
{

}

void Task1Widget::doExecuteTask()
{
    //Prepare data for sentistrength
    QStringList argss;
    argss << "-i";
    argss << QUrl::fromLocalFile(m_datasetDir.path() + "\\Datafiniti_Hotel_Reviews_Jun19.csv").toLocalFile();
    argss << "-o";
    argss << QUrl::fromLocalFile(m_datasetDir.path() + "\\output_sample.txt").toLocalFile();

    m_runner->runPythonScript(m_scriptsDir.path() + "\\parse_csv_for_sentistrength.py", argss);
}
