#ifndef TASK9WIDGET_H
#define TASK9WIDGET_H

#include "taskwidget.h"

class Task9Widget : public TaskWidget
{
    Q_OBJECT
public:
    explicit Task9Widget(QWidget *parent = nullptr, const QString &taskName = QString());

protected:
    virtual void doExecuteTask();
};

#endif // TASK9WIDGET_H
