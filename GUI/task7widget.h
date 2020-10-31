#ifndef TASK7WIDGET_H
#define TASK7WIDGET_H

#include "taskwidget.h"

class Task7Widget : public TaskWidget
{
    Q_OBJECT
public:
    explicit Task7Widget(QWidget *parent = nullptr, const QString &taskName = QString());

protected:
    virtual void doExecuteTask();
};

#endif // TASK7WIDGET_H
