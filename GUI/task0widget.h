#ifndef TASK0WIDGET_H
#define TASK0WIDGET_H

#include "taskwidget.h"

class Task0Widget : public TaskWidget
{
    Q_OBJECT
public:
    Task0Widget(QWidget *parent = nullptr, const QString &taskName = QString());

    // TaskWidget interface
protected:
    void doExecuteTask() override;
};

#endif // TASK0WIDGET_H
