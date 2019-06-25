# OJ Sample judging image

This image serves as a base for grading student submissions. 
There are many hardcoded restrictions so please do read this document! 
If in doubt, you can consult the reference implementation.

## Hardcoded stuff

### `/submission` directory

Student submission will be placed here. 
Please note that student may name their program entry point (or anything) arbitrarily! 
It's up to you to force them to use one you can understand! 
Of course this means nothing for those ecosystems that enforce a naming convention.

### `ENTRYPOINT` and `CMD` instructions in Dockerfile

Neither will change anything, as they will be overwritten by the OJ. Just don't use it.

### `/judge/$STAGE` executables

These will be scripts or binaries that takes no argument. 
These executables ought to be provided by YOU.
They will be called at their respective stage.

### `WORKDIR`

OJ will enforce a working directory at `/judge` at stage change. 
You could of course change it but the change would be lost when the next stage comes.

The working dirctory at first stage is of course defined by your upstream image.

## How does this image works

Most mechanisms can be replaced by your custom mechanisms, but the overall workflow must remain the same. A full judging run is made up of 4 stages.

Please notice that stderr and stdout will be merged in the resulting log, with the exception of grade stage, at which the stdout is a single number as score while stderr will be treated as error log.

### Stage Genesis

During this stage, the Dockerfile is ran on the judging servers you have designated. 
However, those scripts/programs specified in ENTRYPOINT instruction will not run now.

Typically, you'd wish to install everything needed by the grading scripts and some library or building tools students may need. 

If you wish, you could also dynamically generate a reference output based on a reference program and a reference input. Using randomly generated reference input is not advised as it could break the reference program unless you put unnecessarily large amount of person-hours into improving it.

Remember, if you want something in this folder to be available in later stages to grading scripts, you have to COPY them.

Unlike all other stages, this stage will be run AT MOST ONCE PER JUDGING SERVER. The built image will be cached at your judging server.

### Stage Setup

From this stage on, you will not touch Dockerfile anymore. 
Instead, you have to provide an executable (script or program) placed at `/judge/setup` that do whatever you need at this stage.

During this stage, the student submission is taken from his git repo and placed into `/submission` folder.
The grading script should setup student-defined dependencies but DO NOT compile his program. 
If setup/compile/whatsoever failed and the grading script exited with a nonzero return code, student gets 0 score and a big red Compile Error. 
As a consequence, this stage should not involve actual running the main program of student or he may get a confusing error.

If your assignment also requires some other setup, e.g. a service, you should do it now.

Since this stage has network connection, do NOT run arbitrary code submitted.
You should also be wary of certain tool's capability of running arbitrary code (code not from the upstream) when installing packages.
e.g. `pip install /submission` could cause the setup.py there be executed, in a trusted environment. 
That's why we have stage `build` for it.

**This is the most dangerous stage, as this stage has network AND run commands based on student's request. Treat every student as potential cheaters!**

This stage will be run once per recorded submission, provided previous stage didn't fail.

### Stage Build

From this stage on, the network connection will be cut.

During this stage, you should build the student's program using whatever tool you'd like.

Be wary that reference output is avaliable.
You should therefore run the build under another user and chmod reference stuff 400 (or 500).

This stage will be run once per recorded submission, provided previous stages didn't fail.

### Stage Run
During this stage, you run the student homework, preferably under another user, but please don't grade it yet. 

This stage has no network connection!

**Don't do anything else.**

Exiting with nonzero code at this stage will have various meanings:

    RESULT_CPU_TIME_LIMIT_EXCEEDED = 1
    RESULT_REAL_TIME_LIMIT_EXCEEDED = 2
    RESULT_MEMORY_LIMIT_EXCEEDED = 3
    RESULT_RUNTIME_ERROR = 4
    RESULT_SYSTEM_ERROR = 5

All others will be treated as Unknown Runtime Error.

This stage will be run once per recorded submission, provided previous stages didn't fail.

### Stage grade
During this stage, you grade the student output from previous stage. 
Print each test case as `index, score, max_score, error code`.
Please consult `grading/utils.py` on what `error code` can be.
Exiting with nonzero will grant student a Unknown Error and zero score.

This stage still has no network connection!
 
This stage will be run once per recorded submission, provided previous stages didn't fail.

## Writing back info

As a convention, containers log info by printing it to console. 
Please don't log critical info like your testcases, as they will all be displayed to the student.

