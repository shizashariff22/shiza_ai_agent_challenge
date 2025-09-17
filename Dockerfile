# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files into container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports (Flask=5000, Streamlit=8501)
EXPOSE 5000
EXPOSE 8501

# Start both Flask (backend) + Streamlit (frontend)
CMD ["sh", "-c", "python app.py & streamlit run ui.py --server.port=8501 --server.address=0.0.0.0"]

