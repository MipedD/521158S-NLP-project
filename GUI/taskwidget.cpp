#include "taskwidget.h"

#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QPushButton>
#include <QLabel>

#include <QDebug>

TaskWidget::TaskWidget(QWidget *parent, const QString &taskName)
    : QWidget(parent),
      m_runner(nullptr),
      m_taskDescription(nullptr),
      m_taskName(taskName),
      m_executeButton(nullptr)
{
    const QString btnText = "Execute %1";
    const QString titleText ="Step: %1";

    QWidget *background = new QWidget(this);
    QHBoxLayout *bgLayout = new QHBoxLayout;

    QLabel *title = new QLabel(this);
    title->setText(titleText.arg(m_taskName));
    QFont titleFont = title->font();
    titleFont.setPointSize(12);
    title->setFont(titleFont);

    QVBoxLayout *layout = new QVBoxLayout;
    m_taskRequirements = new QTextEdit(this);
    m_taskRequirements->setReadOnly(true);
    m_taskRequirements->setText("Requirements go here");
    m_taskRequirements->setVisible(false);
    m_taskDescription = new QTextBrowser(this);
    m_taskDescription->setReadOnly(true);
    m_taskDescription->setText("Description goes here");
    m_taskDescription->setTextInteractionFlags(m_taskDescription->textInteractionFlags() | Qt::LinksAccessibleByMouse);
    m_taskDescription->setOpenExternalLinks(true);
    m_executeButton = new QPushButton(this);
    m_executeButton->setText(btnText.arg(m_taskName));
    QObject::connect(m_executeButton, &QPushButton::clicked,
                     this, &TaskWidget::executeTask);

    bgLayout->addWidget(m_taskDescription, 2);
    bgLayout->addWidget(m_taskRequirements, 1);
    background->setLayout(bgLayout);
    layout->addWidget(title);
    layout->addWidget(background);
    layout->addWidget(m_executeButton);
    setLayout(layout);
}

void TaskWidget::setScriptRunner(PythonScriptRunner *scriptRunner)
{
    m_runner = scriptRunner;
    connect(m_runner, &PythonScriptRunner::started, [this]{
        this->m_executeButton->setDisabled(true);
    });

    connect(m_runner, &PythonScriptRunner::completed, [this]{
        this->m_executeButton->setEnabled(true);
    });
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
    const QString heading("<h3>Description</h3>");
    m_taskDescription->setHtml(heading+description);
}

void TaskWidget::setRequirements(const QStringList &requirements)
{
    bool canSetRequirements = !requirements.isEmpty();
    m_taskRequirements->setVisible(canSetRequirements);
    if(!canSetRequirements){
        m_taskRequirements->setHtml(QString());
        return;
    }

    const QString heading = "<h3>Requirements</h3>";
    const QString htmlStart = "<ul>";
    const QString htmlEnd = "</ul>";

    QString items;
    for(auto requirement : requirements){
        items.append(QString("<li>%1</li>").arg(requirement));
    }

    m_taskRequirements->setHtml(heading+htmlStart+items+htmlEnd);
}

void TaskWidget::appendResults(const QString &result)
{
    QString prefix("=>");
    m_taskDescription->append(prefix+result);
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
