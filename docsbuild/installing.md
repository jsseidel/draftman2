# Installing Draftman2

Draftman2 will run out-of-the-box in Ubuntu 18.04 and 20.04. Simply clone the
repo and run `draftman2_py_run`.

On other distros, you might need to perform the equivalent of the following:

```
cd draftman2
sudo apt install debhelper libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0 python3-gi python3-gi-cairo
pip install -r requirements.txt
```
