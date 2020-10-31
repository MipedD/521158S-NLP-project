#ifndef TASK1WIDGET_H
#define TASK1WIDGET_H

#include <QWidget>
#include <QDir>

#include "taskwidget.h"
#include "pythonscriptrunner.h"

class Task1Widget : public TaskWidget
{
    Q_OBJECT
public:
    explicit Task1Widget(QWidget *parent = nullptr, const QString &taskName = QString());

protected:
    virtual void doExecuteTask();
};

#endif // TASK1WIDGET_H
