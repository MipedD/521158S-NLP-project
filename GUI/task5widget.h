#ifndef TASK5WIDGET_H
#define TASK5WIDGET_H

#include "taskwidget.h"

class Task5Widget : public TaskWidget
{
    Q_OBJECT
public:
    explicit Task5Widget(QWidget *parent = nullptr, const QString &taskName = QString());

protected:
    virtual void doExecuteTask();
};

#endif // TASK5WIDGET_H
