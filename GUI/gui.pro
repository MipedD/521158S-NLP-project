QT += widgets

CONFIG += c++11 console
CONFIG -= app_bundle

# The following define makes your compiler emit warnings if you use
# any Qt feature that has been marked deprecated (the exact warnings
# depend on your compiler). Please consult the documentation of the
# deprecated API in order to know how to port your code away from it.
DEFINES += QT_DEPRECATED_WARNINGS

# You can also make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
# You can also select to disable deprecated APIs only up to a certain version of Qt.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
        main.cpp \
        pythonscriptrunner.cpp \
        task0widget.cpp \
        task10widget.cpp \
        task12widget.cpp \
        task1widget.cpp \
        task2widget.cpp \
        task3widget.cpp \
        task4widget.cpp \
        task5widget.cpp \
        task7widget.cpp \
        task8widget.cpp \
        task9widget.cpp \
        taskwidget.cpp

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

HEADERS += \
    pythonscriptrunner.h \
    task0widget.h \
    task10widget.h \
    task12widget.h \
    task1widget.h \
    task2widget.h \
    task3widget.h \
    task4widget.h \
    task5widget.h \
    task7widget.h \
    task8widget.h \
    task9widget.h \
    taskwidget.h

RESOURCES += \
    resources.qrc
