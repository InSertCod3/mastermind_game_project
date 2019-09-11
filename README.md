# Mastermind Project

### Creating the Backend database
```code
>>> cd mastermind_backend
>>> pip install -r requirements.txt
>>> python manage.py migrate
>>> python manage.py migrate --run-syncdb
```

### Starting the Backend
```code
>>> cd mastermind_backend
>>> python manage.py runserver
```

### Starting the Fronend
```code
>>> cd mastermind_frontend
>>> npm install
>>> yarn start || npm start
```