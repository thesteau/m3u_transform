# Base image
FROM node:20-slim

# Set working directory
WORKDIR /app

# Install Node.js dependencies
COPY app/package.json ./package.json
RUN npm install

# Copy Node.js app
COPY app/ ./app/

# Copy private script directory
COPY m3u_script/ ./m3u_script/

# Install Python dependencies for the script
RUN apt-get update && apt-get install -y python3.11 python3-pip
RUN pip3 install --break-system-packages -r ./m3u_script/requirements.txt

# Expose port
EXPOSE 5000

# Run the Node.js server
CMD ["node", "./app/server.js"]
