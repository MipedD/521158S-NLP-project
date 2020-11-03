#include "task10widget.h"

Task10Widget::Task10Widget(QWidget *parent, const QString &taskName)
    : TaskWidget(parent, taskName)
{
    const QString description =
            "For task 10 each review is split into one of two classes: ambiguous or non-ambiguous. "
            "Whether a review belongs in the ambiguous class is determined by whether sentiment analyzer VADER "
            "result has significant deviation from the users rating.<br><br>"

            "Additionally in task 10 it is tested whether reviews in ambiguous class are likely to be badly written. "
            "Whether a review is badly written is determined by the percetange of known words in the review. A word is considered "
            "known if WordNet is able to find any synsets for the word. A word without synsets is considered unknown.<br><br>"

            "Finally for task 11 it is checked whether ambiguous reviews are likely to be shorter than others.";
    setDescription(description);
}

void Task10Widget::doExecuteTask()
{
    QStringList args;
    args << "-i";
    args << QUrl::fromLocalFile(m_datasetDir.path() + "\\dataset_processed.csv").toLocalFile();
    args << "-o";
    args << QUrl::fromLocalFile(m_datasetDir.path() + "\\dataset_processed.csv").toLocalFile();

    connect(m_runner, &PythonScriptRunner::completed, this, &Task10Widget::executePart2);
    m_runner->runPythonScript(m_scriptsDir.path() + "\\ambiguous_class.py", args);
}

void Task10Widget::executePart2()
{
    disconnect(m_runner, &PythonScriptRunner::completed, this, &Task10Widget::executePart2);
    QStringList args;
    args << "-i";
    args << QUrl::fromLocalFile(m_datasetDir.path() + "\\dataset_processed.csv").toLocalFile();
    args << "-o";
    args << QUrl::fromLocalFile(m_datasetDir.path() + "\\recognized_words.csv").toLocalFile();

    m_runner->runPythonScript(m_scriptsDir.path() + "\\unrecognized_words.py", args);
}
