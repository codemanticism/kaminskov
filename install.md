> [ALERT]
> This is still experimental.

#To install it, the environment has to support all of this:
* time
* sys (needs to read arguments)
* subprocess
* signal
* locale
* tkinter
* threading
* time
* re
* curses
I recommend using the project https://docs.conda.io/projects/conda/en/stable/index.html to then use Nuitka thru `python3 -m nuitka main.py` to then compile the code to make it run faster, because I found that it is more predictable than PyPy, which instead uses JIT compilation.
CPython does currently have a JIT compiler, but it is experimental, as of what I have seen, as of December 2025.
> [NOTICE]
> Replace with ~ what you want.

```bash
cd ~
git clone git@github.com:codemanticism/kaminskov.git
cd kaminskov
python3 -m nuitka main.py
chmod u+x main.sh
mv main.sh /usr/local/bin/kaminskov
kaminskov
```
