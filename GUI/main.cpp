#include <QApplication>
#include <QStringList>
#include <QCommandLineParser>
#include <QFileInfo>
#include <QTextEdit>
#include <QVBoxLayout>
#include <QTabWidget>
#include <QUrl>
#include <QPushButton>
#include <QDebug>

#include "pythonscriptrunner.h"
#include "task1widget.h"
#include "task0widget.h"
#include "task2widget.h"
#include "task4widget.h"
#include "task10widget.h"
#include "task12widget.h"

void setupTaskWidget(TaskWidget *task, QTabWidget *tabWidget, PythonScriptRunner *runner)
{
    task->setScriptRunner(runner);
    task->setScriptsDirectory(tabWidget->property("scriptDir").toString());
    task->setDatasetDirectory(tabWidget->property("dataDir").toString());
    tabWidget->addTab(task, task->taskName());
}

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    QString dataSetDir;
    QString scriptsDir;
    QString errorMsg;

    //Parse command line arguments & ensure they're somewhat solid
    QCommandLineParser clParser;
    QCommandLineOption clOptionDatasetDir("d");
    clOptionDatasetDir.setValueName("dataset directory");
    QCommandLineOption clOptionScriptDir("s");
    clOptionScriptDir.setValueName("scripts directory");

    clParser.addOption(clOptionDatasetDir);
    clParser.addOption(clOptionScriptDir);

    clParser.process(a);

    dataSetDir = clParser.value(clOptionDatasetDir);
    scriptsDir = clParser.value(clOptionScriptDir);

    errorMsg = dataSetDir.isEmpty() ? "Please specify directory where datasets are located." : QString();
    errorMsg = scriptsDir.isEmpty() ? "Please specify directory where scripts are located." : QString();

    if(!errorMsg.isEmpty()){
        qWarning() << errorMsg;
        return 2;
    }

    QFileInfo dir1(dataSetDir);
    QFileInfo dir2(scriptsDir);

    if(!dir1.isDir() || !dir2.isDir()){
        qWarning() << "Dataset directory and scripts directory need to be real directories.";
        return 2;
    }

    PythonScriptRunner scriptRunner;

    //Basic gui
    QWidget root;
    QVBoxLayout *layout = new QVBoxLayout;
    QTextEdit *logView = new QTextEdit(&root);
    QPushButton *clearLogBtn = new QPushButton(&root);
    QObject::connect(clearLogBtn, &QPushButton::clicked, [logView]{
        logView->clear();
    });
    clearLogBtn->setText("Clear log");
    logView->setReadOnly(true);

    QTabWidget *tasksTabWidget = new QTabWidget(&root);
    tasksTabWidget->setProperty("dataDir", dataSetDir);
    tasksTabWidget->setProperty("scriptDir", scriptsDir);
    //List of tasks
    QVector<TaskWidget*> tasks;
    tasks << new Task0Widget(tasksTabWidget, "Preparation");
    tasks << new Task1Widget(tasksTabWidget, "Task 1");
    tasks << new Task2Widget(tasksTabWidget, "Task 2");
    tasks << new Task4Widget(tasksTabWidget, "Task 4");
    tasks << new Task10Widget(tasksTabWidget, "Task 10");
    tasks << new Task12Widget(tasksTabWidget, "Task 12");
    //Setup each task in gui
    for(auto task : tasks) {
        setupTaskWidget(task, tasksTabWidget, &scriptRunner);
    }

    //Add everything to layout
    layout->addWidget(tasksTabWidget);
    layout->addWidget(logView);
    layout->addWidget(clearLogBtn);

    //Append output to log view
    QObject::connect(&scriptRunner, &PythonScriptRunner::pythonOutput, [logView](const QString &output){
        logView->append(output);
    });

    root.resize(640, 480);
    root.setLayout(layout);
    root.show();

    return a.exec();
}
