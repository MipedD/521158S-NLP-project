#include "pythonscriptrunner.h"

PythonScriptRunner::PythonScriptRunner(QObject *parent) : QObject(parent)
{

}

void PythonScriptRunner::runPythonScript(const QString &scriptname, const QStringList &args)
{
    QStringList completeArgs(args);
    QProcess *pythonProcess = new QProcess(this);
    pythonProcess->setProcessChannelMode(QProcess::ProcessChannelMode::MergedChannels);
    pythonProcess->setProgram("python.exe");
    completeArgs.insert(0, scriptname);

    pythonProcess->setArguments(completeArgs);

    pythonOutput("--- Starting python.exe ---\n");

    QObject::connect(pythonProcess, &QProcess::stateChanged, [this,pythonProcess](QProcess::ProcessState state){
        switch(state)
        {
        case QProcess::ProcessState::NotRunning:
            pythonProcess->deleteLater();
            pythonOutput("--- python.exe finished ---\n");
            completed();
            Q_FALLTHROUGH();
        default:
            break;
        }
    });

    QObject::connect(pythonProcess, &QProcess::readyRead, [this, pythonProcess]{
        pythonOutput(pythonProcess->readAll());
    });

    pythonProcess->start();
}
