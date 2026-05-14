## 1 Prepare
- Requriements
- python -m venv venv
- source venv/bin/activate
- venv\Scripts\activate


## 2 dependencies

# Install dependencies
- pip install -r requirements.txt

# Set up database (run once)
python db/setup_db.py

# Set up Streamlit secrets
mkdir .streamlit
# Create .streamlit/secrets.toml with your DB credentials

## RUN
streamlit run app.py