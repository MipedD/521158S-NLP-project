#ifndef PYTHONSCRIPTRUNNER_H
#define PYTHONSCRIPTRUNNER_H

#include <QObject>
#include <QProcess>

class PythonScriptRunner : public QObject
{
    Q_OBJECT

public:
    PythonScriptRunner(QObject *parent = nullptr);
    void runPythonScript(const QString &scriptname, const QStringList &args);
    void writeToLog(const QString &str);
    QString parseResults(const QByteArray &input);

signals:

    void started();
    void pythonOutput(const QString &output);
    void result(const QString &result);
    void completed();
};

#endif // PYTHONSCRIPTRUNNER_H
