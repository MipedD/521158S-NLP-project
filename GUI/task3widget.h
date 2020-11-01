#ifndef TASK3WIDGET_H
#define TASK3WIDGET_H

#include "taskwidget.h"

class Task3Widget : public TaskWidget
{
    Q_OBJECT
public:
    explicit Task3Widget(QWidget *parent = nullptr, const QString &taskName = QString());

protected:
    virtual void doExecuteTask();
    virtual void displayGraph();
};

#endif // TASK3WIDGET_H
