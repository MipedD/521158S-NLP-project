#ifndef TASK10WIDGET_H
#define TASK10WIDGET_H

#include "taskwidget.h"

class Task10Widget : public TaskWidget
{
    Q_OBJECT
public:
    Task10Widget(QWidget *parent = nullptr, const QString &taskName = QString());

    // TaskWidget interface
protected:
    void doExecuteTask() override;
    void executePart2();
};

#endif // TASK10WIDGET_H
