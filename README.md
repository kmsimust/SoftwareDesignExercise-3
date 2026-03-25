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


### 3. get into backend directory.
```python
cd backend
```


### 4. install the requirements.
```python
pip install -r .\requirements.txt
```

if some still missing after try running server, use this.

```python
python -m pip install ...
```


### 5. migrate the sqlite3.
make tables for sqlite3.
```bash
python manage.py migrate 
```


### 6. run the testing server.
make sure you're in the same directory as manage.py, in this case is backend.
```bash
python manage.py runserver 
```


## Demo Screenshots

Inserting Data into Tables
![Adding Tables](Demo/Adding_Tables.png)

User Tables
![Users](Demo/Users.png)

Library Tables
![Library User1](Demo/Library_User1.png)

Song Tables
![Songs](Demo/Songs.png)


$${\color{white}End}$$