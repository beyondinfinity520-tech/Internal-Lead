# Use the official Apify Python image with Selenium and Chrome pre-installed
FROM apify/actor-python-selenium:3.11

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt ./

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . ./

# Set the default command. 
# NOTE: This can be overridden in the Apify Console.
# By default, we run the main scraper actor.
CMD ["python", "main.py"]