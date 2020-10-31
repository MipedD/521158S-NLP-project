#ifndef TASK6WIDGET_H
#define TASK6WIDGET_H

#include "taskwidget.h"

class Task6Widget : public TaskWidget
{
    Q_OBJECT
public:
    explicit Task6Widget(QWidget *parent = nullptr, const QString &taskName = QString());

protected:
    virtual void doExecuteTask();
};

#endif // TASK6WIDGET_H
