# Backend (Django)

## How to run/install


### 1. create python enviroment in backend directory.
```python
python -m venv .venv 
```

".venv" is environment directory name.


### 2. activate environment in terminal.
```python
.\.venv\Scripts\activate
```
in command prompt  
"(.venv) PS D:\directory>" should show up like this.


### 3. install the requirements.
```python
pip install -r .\requirements.txt
```

if some still missing after try running server, use this.

```python
python -m pip install ...
```

### 4. migrate the sqlite3.
make tables for sqlite3.
```bash
python manage.py migrate 
```

### 5. run the testing server.
make sure you're in the same directory as manage.py, in this case is backend.
```bash
python manage.py runserver 
```
$${\color{white}End}$$
