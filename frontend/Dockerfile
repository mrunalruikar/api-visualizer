# Use an official Nginx runtime as a parent image
FROM nginx:alpine

# Remove the default nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Copy our custom configuration file
COPY nginx.conf /etc/nginx/conf.d/

# Copy the static content from the frontend directory into the Nginx html directory
COPY . /usr/share/nginx/html

# Expose port 80 for the web server
EXPOSE 80
