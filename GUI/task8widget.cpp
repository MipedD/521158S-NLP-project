#include "task8widget.h"

Task8Widget::Task8Widget(QWidget *parent, const QString &taskName)
    : TaskWidget(parent, taskName)
{
    const QString description =
            "In task 8 the hypothesis that the presence of a given named-entity "
            "within a review would entail positive or negative sentiment is tested. "
            "This is done by checking whether some category of named-entities "
            "appears more frequently either in positive or negative reviews. "
            "Again, negative reviews are considered those with user rating less or equal to "
            "two and positive when the rating is equal or greater to 4 (on scale 1-5).";

    setDescription(description);

    QStringList requirements;
    requirements << "Preparation step completed";
    requirements << "All previous steps";
    setRequirements(requirements);
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
