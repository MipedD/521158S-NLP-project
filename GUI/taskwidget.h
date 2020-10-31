#ifndef TASKWIDGET_H
#define TASKWIDGET_H

#include <QWidget>
#include <QTextEdit>
#include <QDir>

#include "pythonscriptrunner.h"

class TaskWidget : public QWidget
{
    Q_OBJECT
public:
    explicit TaskWidget(QWidget *parent = nullptr, const QString &taskName = QString());
    void setScriptRunner(PythonScriptRunner *runner);
    void setDatasetDirectory(const QDir &directory);
    void setScriptsDirectory(const QDir &directory);
    void setDescription(const QString &description);
    void setRequirements(const QStringList &requirements);
    void appendResults(const QString &results);
    QString taskName() const;

private slots:
    void executeTask();

protected:
    virtual void doExecuteTask();

protected:
    PythonScriptRunner *m_runner;
    QDir m_scriptsDir;
    QDir m_datasetDir;
    QTextEdit *m_taskDescription;
    QTextEdit *m_taskRequirements;
    QString m_taskName;
};

#endif // TASKWIDGET_H
