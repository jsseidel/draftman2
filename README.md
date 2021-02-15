# draftman2

A minimalist draft-management application I use to help me organize long writing
projects. It may or may not be useful to others. Draftman2 is BETA software, so if
you decide to try it, be sure to turn on backups.

[https://jsseidel.github.io/draftman2/](https://jsseidel.github.io/draftman2/)

# Running Draftman2

Draftman2 will run as-is in Ubuntu 18.04/20.04 with no additional
requirements:

```
./draftman2_py_run
```

On other distros, or if you use a virtual environment, you might need to
perform the equivalent of the following:

```
sudo apt install libgirepository1.0-dev gcc libcairo2-dev python3-dev gir1.2-gtk-3.0 python3-gi python3-gi-cairo
cd draftman2
pip3 install wheel
pip3 install -r requirements.txt
```

