#include "task1widget.h"

#include <QVBoxLayout>
#include <QTextEdit>
#include <QPushButton>

Task1Widget::Task1Widget(QWidget *parent)
    : QWidget(parent),
      runner(nullptr)
{
    QVBoxLayout *layout = new QVBoxLayout;
    QTextEdit *description = new QTextEdit(this);
    description->setReadOnly(true);
    description->setText("lorem ipsum");
    QPushButton *executeBtn = new QPushButton(this);
    executeBtn->setText("Execute task 1");
    QObject::connect(executeBtn, &QPushButton::clicked,
                     this, &Task1Widget::executeTask1);

    layout->addWidget(description);
    layout->addWidget(executeBtn);
    setLayout(layout);
}

void Task1Widget::setScriptRunner(PythonScriptRunner *a_runner)
{
    runner = a_runner;
}

void Task1Widget::setDatasetDirectory(const QDir &directory)
{
    datasetDir = directory;
}

void Task1Widget::setScriptsDirectory(const QDir &directory)
{
    scriptsDir = directory;
}

void Task1Widget::executeTask1()
{
    //Prepare data for sentistrength
    QStringList argss;
    argss << "-i";
    argss << QUrl::fromLocalFile(datasetDir.path() + "\\Datafiniti_Hotel_Reviews_Jun19.csv").toLocalFile();
    argss << "-o";
    argss << QUrl::fromLocalFile(datasetDir.path() + "\\output_sample.txt").toLocalFile();
    argss << "-c";
    argss << "reviews.text";

    runner->runPythonScript(scriptsDir.path() + "\\parse_csv_for_sentistrength.py", argss);
}
