For windows users:

1. Run Docker QuickStart Terminal - this way this instructions work (else use \ and step 3 will require .bat)

2. Go to docs
```
cd /c/Users/yhasan/st2docs
```
3. activate virtualenv: 
```
. virtualenv/Scripts/activate
```
4. Run 
```
sphinx-autobuild -H 127.0.0.1 -b html ./docs/source/ ./docs/build/html
```
5. Connect to http://localhost:8000 Edit files. Watch live updates. Enjoy.

### Setting up
sphinx-autobuild -H 0.0.0.0 -t enterprise -b html ./docs/source/ ./docs/build/html