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

    QString scriptInfo("Running %1 with arguments:\n %2");
    QString argsStr;
    for(auto str : args)
        argsStr.append(str + "\n");

    pythonOutput(scriptInfo.arg(scriptname).arg(argsStr));

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
        while(pythonProcess->canReadLine()){
            QByteArray line = pythonProcess->readLine();
            pythonOutput(parseResults(line));
        }
    });

    pythonProcess->start();
    started();
}

void PythonScriptRunner::writeToLog(const QString &str)
{
    pythonOutput(str);
}

QString PythonScriptRunner::parseResults(const QByteArray &input)
{
    QHash<QString, QString> highlightForTag;
    highlightForTag.insert("<%1result>", "green");

    QString output(input);

    const QString span("<span style=\"color:%1\">");

    for(auto tag : highlightForTag.keys()){
        if(output.contains(tag.arg(""))){
            output.replace(tag.arg(""),span.arg(highlightForTag.value(tag)));
            output.replace(tag.arg("/"), "</span>");
            result(output);
        }
    }

    return output;
}
