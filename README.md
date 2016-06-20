##*ART*##

ART is the software for Automation on RF Tests.  
It has been three years since the initial development of the software.
Now, it is released for its first alpha version (15.a1).

Currently, it does only VNA sweep.  More test cases will be soon added.
Based on the design of the software structure, more instrumentation drivers can be added easily.
If you have any RF test automation requirements, please contact me.  
I will make demanded requests a high priority.

![alt tag](/quick_look.jpg)


**Features:**

1. Project management - tests can be managed as a project. All the tests related to the specific system or component can be managed in one project.  

2. Batch tests - tests can be added in one batch.  'Green Light' feature can be enabled to allow continual repeated tests without prompt interface interruption.  Suitable for repeatability and reliability tests.

3. Easy measurement interface - the design concept of ART is to provide simple interface to start a test.  ART will remember the major measurement and equipment settings.

4. Future - add graph GUI to render the output graphs.

5. Future - add tools to analyze data, such as standard deviations of big quantity of batch tests.

6. Future - add GUI to display test system diagrams.


**Prerequisite:**

1. Python 2.7.x

2. pyvisa 1.6.x

3. wxPython 3.0.x

4. matplotlib 1.4.x


**Usage:**

Retrieve git repository.
```
git clone https://github.com/antopenrf/ART.git
```

Then start the program.
```
cd ART
python art.py
```


