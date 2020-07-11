# draftman2

A minimalist draft-management application for long-form writers, currently in beta release.

[https://jsseidel.github.io/draftman2/](https://jsseidel.github.io/draftman2/)

# Running Draftman2

Draftman2 will run as is in Ubuntu 18.04/20.04 with no additional
requirements:

```
./draftman2_py_run
```

On other distros, you might need to perform the equivalent of the following:

```
cd draftman2
sudo apt install debhelper libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0 python3-gi python3-gi-cairo
pip install -r requirements.txt
```
