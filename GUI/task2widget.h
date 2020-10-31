#ifndef TASK2WIDGET_H
#define TASK2WIDGET_H

#include "taskwidget.h"

class Task2Widget : public TaskWidget
{
    Q_OBJECT
public:
    explicit Task2Widget(QWidget *parent = nullptr, const QString &taskName = QString());

protected:
    virtual void doExecuteTask();
};


#endif // TASK2WIDGET_H
