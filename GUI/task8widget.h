#ifndef TASK8WIDGET_H
#define TASK8WIDGET_H

#include "taskwidget.h"

class Task8Widget : public TaskWidget
{
    Q_OBJECT
public:
    Task8Widget(QWidget *parent = nullptr, const QString &taskName = QString());

    // TaskWidget interface
protected:
    void doExecuteTask() override;
};

#endif // TASK8WIDGET_H
