# Instructions

For this project, you need to have Python (3.8 or higher) and Node.js (14.x or higher) installed on your machine.

Create virtual env: 
```
cd backend
python -m venv venv
```
Activate the virtual env:

```
Windows: venv\Scripts\activate 
```
```
Linux/macOs: source venv/bin/activate
```
Install backend dependencies:
```
pip install -r requirements.txt
```
Populate database with random entries:

```
python manage.py populate_data
```
Run the backend server:
```
python manage.py runserver

```
Install frontend dependencies
```
cd ../frontend
npm install
npm run serve
```
Run on browser on port 8080