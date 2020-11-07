#include "task9widget.h"

Task9Widget::Task9Widget(QWidget *parent, const QString &taskName)
    : TaskWidget(parent, taskName)
{
    const QString description =
            "In this task the hypothesis that negative reviews entail argumentation will be tested. "
            "There is a short list of explanation inducing expressions put together in %1 "
            "and each review in the dataset is tested for the number of these expressions found."
            "<br><br>"
            "Note: reviews are in the scale of 1-5 and positive are &gt;=4 and negative are &lt;=2.";

    setDescription(description.arg("explanatory_wording.csv"));

    QStringList requirements;
    requirements << "Preparation step completed";
    requirements << "All previous steps";
    setRequirements(requirements);
}

void Task9Widget::doExecuteTask()
{
    QStringList args;
    args << "-i";
    args << QUrl::fromLocalFile(m_datasetDir.path() + "\\dataset_processed.csv").toLocalFile();
    args << "-e";
    args << QUrl::fromLocalFile(m_datasetDir.path() + "\\explanatory_wording.csv").toLocalFile();
    m_runner->runPythonScript(m_scriptsDir.path() + "\\task9.py", args);
}
