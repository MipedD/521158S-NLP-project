#include "task3widget.h"

#include <QLabel>

Task3Widget::Task3Widget(QWidget *parent, const QString &taskName)
    : TaskWidget(parent, taskName)
{
    const QString description =
            "In this task the Vader and SentiStrength results are going to be plotted in the same graph along with the actual reviews. "
            "The results from both analyzers are going to be normalized along with the actual reviews to get a more meaningful graph. "
            "The graph will only contain the first 1000 points of the dataset as plotting the results for all 10 000 values wouldn't look "
            "very informative at all. <br><br>"
            "Additionally pearson coefficient correlation is calculated for both analyzer results in relation to the user ratings.";
    setDescription(description);

    QStringList requirements;
    requirements << "Preparation step completed";
    requirements << "Task 1 completed";
    requirements << "Task 2 completed";
    setRequirements(requirements);
}

void Task3Widget::doExecuteTask()
{
    QStringList args;
    args << "-i";
    args << QUrl::fromLocalFile(m_datasetDir.path() + "\\dataset_processed.csv").toLocalFile();
    args << "-o";
    args << QUrl::fromLocalFile(m_datasetDir.path() + "\\plot.png").toLocalFile();

    connect(m_runner, &PythonScriptRunner::completed, this, &Task3Widget::displayGraph);
    m_runner->runPythonScript(m_scriptsDir.path() + "\\task3.py", args);
}

void Task3Widget::displayGraph()
{
    disconnect(m_runner, &PythonScriptRunner::completed, this, &Task3Widget::displayGraph);
    QLabel *plot = new QLabel(this);
    plot->setWindowTitle("Sentiment analyzer results and ratings");
    plot->setWindowFlag(Qt::Window, true);
    plot->setAttribute(Qt::WidgetAttribute::WA_DeleteOnClose, true);
    plot->setPixmap(QPixmap(QUrl::fromLocalFile(m_datasetDir.path() + "\\plot.png").toLocalFile()));
    plot->show();
}
