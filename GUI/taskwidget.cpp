#include "taskwidget.h"

#include <QVBoxLayout>
#include <QPushButton>
#include <QLabel>

TaskWidget::TaskWidget(QWidget *parent, const QString &taskName)
    : QWidget(parent),
      m_runner(nullptr),
      m_taskDescription(nullptr),
      m_taskName(taskName)
{
    const QString btnText = "Execute %1";
    const QString titleText ="Step: %1";

    QLabel *title = new QLabel(this);
    title->setText(titleText.arg(m_taskName));
    QFont titleFont = title->font();
    titleFont.setPointSize(12);
    title->setFont(titleFont);

    QVBoxLayout *layout = new QVBoxLayout;
    m_taskDescription = new QTextEdit(this);
    m_taskDescription->setReadOnly(true);
    m_taskDescription->setText("Description goes here");
    QPushButton *executeBtn = new QPushButton(this);
    executeBtn->setText(btnText.arg(m_taskName));
    QObject::connect(executeBtn, &QPushButton::clicked,
                     this, &TaskWidget::executeTask);

    layout->addWidget(title);
    layout->addWidget(m_taskDescription);
    layout->addWidget(executeBtn);
    setLayout(layout);
}

void TaskWidget::setScriptRunner(PythonScriptRunner *scriptRunner)
{
    m_runner = scriptRunner;
}

void TaskWidget::setDatasetDirectory(const QDir &directory)
{
    m_datasetDir = directory;
}

void TaskWidget::setScriptsDirectory(const QDir &directory)
{
    m_scriptsDir = directory;
}

void TaskWidget::setDescription(const QString &description)
{
    m_taskDescription->setText(description);
}

QString TaskWidget::taskName() const
{
    return m_taskName;
}

void TaskWidget::executeTask()
{
    doExecuteTask();
}

void TaskWidget::doExecuteTask()
{

}
