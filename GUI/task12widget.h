#ifndef TASK12WIDGET_H
#define TASK12WIDGET_H

#include "taskwidget.h"

class Task12Widget : public TaskWidget
{
    Q_OBJECT
public:
    Task12Widget(QWidget *parent = nullptr, const QString &taskName = QString());

    // TaskWidget interface
protected:
    void doExecuteTask() override;
};

#endif // TASK12WIDGET_H
