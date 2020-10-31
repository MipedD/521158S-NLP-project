#include "task1widget.h"

#include <QVBoxLayout>
#include <QTextEdit>
#include <QPushButton>

Task1Widget::Task1Widget(QWidget *parent, const QString &taskName)
    : TaskWidget(parent, taskName)
{
    const QString description =
            "In this task each review is going to be run through SentiStrength. "
            "Data is first processed into a format which is recognized by SentiStrength (tab separated CSV) "
            "after which SentiStrength will assess the sentiment polarity for each review individually and write it to the"
            " file parsed for SentiStrength. "
            "After analysis is completed the input file for SentiStrength is read and combined with the main database"
            " and temporary file is deleted as it is now obsolete.";
    setDescription(description);
}

void Task1Widget::doExecuteTask()
{
    //Prepare data for sentistrength
    QStringList argss;
    argss << "-i";
    argss << QUrl::fromLocalFile(m_datasetDir.path() + "\\dataset_processed.csv").toLocalFile();
    argss << "-o";
    argss << QUrl::fromLocalFile(m_datasetDir.path() + "\\temp.csv").toLocalFile();

    m_runner->runPythonScript(m_scriptsDir.path() + "\\parse_csv_for_sentistrength.py", argss);

    connect(m_runner, &PythonScriptRunner::completed, this, &Task1Widget::runSentiStrength);
}

void Task1Widget::runSentiStrength()
{
    disconnect(m_runner, &PythonScriptRunner::completed, this, &Task1Widget::runSentiStrength);

    QStringList args;
    args << "-jar";
    args << QUrl::fromLocalFile(m_scriptsDir.path() + "\\thirdparty\\sentistrengthclient\\sentistrengthcom.jar").toLocalFile();
    args << "sentidata";
    args << QUrl::fromLocalFile(m_scriptsDir.path() + "\\thirdparty\\sentistrengthclient\\sentidata\\").toLocalFile();
    args << "input";
    args << QUrl::fromLocalFile(m_datasetDir.path() + "\\temp.csv").toLocalFile();
    args << "annotateCol";
    args << "3";
    args << "overwrite";
    args << "UTF8";

    QProcess *sentistrength = new QProcess(this);
    sentistrength->setProcessChannelMode(QProcess::ProcessChannelMode::MergedChannels);
    sentistrength->setProgram("java.exe");
    sentistrength->setArguments(args);
    m_runner->pythonOutput("--- Running sentistrength (java.exe) ---\n");

    QObject::connect(sentistrength, &QProcess::stateChanged, [this,sentistrength](QProcess::ProcessState state){
        switch(state)
        {
        case QProcess::ProcessState::NotRunning:
            sentistrength->deleteLater();
            m_runner->pythonOutput("--- java.exe finished ---\n");
            addDataToDb();
            Q_FALLTHROUGH();
        default:
            break;
        }
    });

    QObject::connect(sentistrength, &QProcess::readyRead, [this, sentistrength]{
        m_runner->pythonOutput(sentistrength->readAll());
    });

    sentistrength->start();
}

void Task1Widget::addDataToDb()
{
    QStringList args;
    args << "-i";
    args << QUrl::fromLocalFile(m_datasetDir.path() + "\\temp.csv").toLocalFile();
    args << "-o";
    args << QUrl::fromLocalFile(m_datasetDir.path() + "\\dataset_processed.csv").toLocalFile();
    m_runner->runPythonScript(m_scriptsDir.path() + "\\sentistrength_to_db.py", args);
}
