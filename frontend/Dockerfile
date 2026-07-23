# Use the official Node.js 16 image as the base
FROM node:16

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json files into the container
COPY package*.json ./

# Install project dependencies and globally install Vue CLI
RUN npm install && npm install -g @vue/cli

# Verify Vue CLI installation
RUN vue --version

# Copy the rest of the frontend code into the container
COPY . .

# Expose the port the frontend will run on
EXPOSE 8080

# Default command to start the Vue.js dev server for development mode
CMD ["npm", "run", "serve"]
