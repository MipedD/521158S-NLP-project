#include "task12widget.h"

Task12Widget::Task12Widget(QWidget *parent, const QString &taskName)
    : TaskWidget(parent, taskName)
{
    const QString description =
            "In this task the goal was to test the following hypothesis: ambiguous reviews have bad readability. "
            "This hypothesis is tested by calculating the Automated Readability Index (ARI) for each review and "
            "seeing which class (ambiguous vs non-ambiguous) has the larger value by average. The results are "
            "printed into the output panel below. Additionally the ARI value can be found in the database.";
    setDescription(description);

    QStringList requirements;
    requirements << "Preparation step completed";
    requirements << "All previous steps";
    setRequirements(requirements);
}

void Task12Widget::doExecuteTask()
{
    QStringList args;
    args << "-i";
    args << QUrl::fromLocalFile(m_datasetDir.path() + "\\dataset_processed.csv").toLocalFile();
    args << "-o";
    args << QUrl::fromLocalFile(m_datasetDir.path() + "\\dataset_processed.csv").toLocalFile();
    args << "-c";
    args << "reviews.text";

    m_runner->runPythonScript(m_scriptsDir.path() + "\\textstat_readability.py", args);
}
