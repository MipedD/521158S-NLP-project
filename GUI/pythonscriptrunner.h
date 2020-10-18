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

signals:

    void pythonOutput(const QString &output);
    void completed();
};

#endif // PYTHONSCRIPTRUNNER_H
