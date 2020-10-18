#ifndef TASK1WIDGET_H
#define TASK1WIDGET_H

#include <QWidget>
#include <QDir>

#include "pythonscriptrunner.h"

class Task1Widget : public QWidget
{
    Q_OBJECT
public:
    explicit Task1Widget(QWidget *parent = nullptr);
    void setScriptRunner(PythonScriptRunner *runner);
    void setDatasetDirectory(const QDir &directory);
    void setScriptsDirectory(const QDir &directory);

private slots:

    void executeTask1();

private:
    PythonScriptRunner *runner;
    QDir scriptsDir;
    QDir datasetDir;

};

#endif // TASK1WIDGET_H
