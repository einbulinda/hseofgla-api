# Define the dependencies for the project
contents=(
    "flask"
    "pathlib"
    "python-dotenv"
    "PyJWT"
    "Flask-SQLAlchemy"
    "Flask-Migrate"
    "flask-bcrypt"
    "psycopg2-binary"
)

echo "[ `date` ]": "START"
echo "[ `date` ]": "Creating virtual env"
python -m venv venv/
echo "[ `date` ]": "Creating folders and files"
python template.py
# Write contents to requirements.txt
printf "%s\n" "${contents[@]}" > requirements.txt
echo "[ `date` ]" : "requirements.txt file created successfully!"
echo "[ `date` ]" : "Installing the requirements"
echo "[ `date` ]": "Activating the virtual environment"
source venv/Scripts/activate
pip install -r requirements.txt
echo "[ `date`]":"Deactivating virtual environment"
deactivate
echo "[ `date` ]": "END"