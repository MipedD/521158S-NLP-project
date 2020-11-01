#ifndef TASK4WIDGET_H
#define TASK4WIDGET_H

#include "taskwidget.h"

class Task4Widget : public TaskWidget
{
    Q_OBJECT
public:
    explicit Task4Widget(QWidget *parent = nullptr, const QString &taskName = QString());

protected:
    virtual void doExecuteTask();
    virtual void extractDifferentCategories();
};


#endif // TASK4WIDGET_H
