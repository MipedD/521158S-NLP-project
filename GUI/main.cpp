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
    //Tab for task 1
    Task1Widget *t1w = new Task1Widget;
    t1w->setScriptRunner(&scriptRunner);
    t1w->setDatasetDirectory(QDir(dataSetDir));
    t1w->setScriptsDirectory(QDir(scriptsDir));
    tasksTabWidget->addTab(t1w, "Task 1");
    //Tab for task 2
    // etc etc

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