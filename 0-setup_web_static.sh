#!/usr/bin/env bash
# Sets up web servers for static deployment

# Setup root privilege
if [ "$(id -u)" -ne 0 ]; then
	echo "This script must be run as root."
	exit 0
fi

# Install nginx if not installed
if ! dpkg -l nginx; then
	echo "Nginx not installed, installing..."
	apt update && apt -y upgrade
	apt -y install nginx
fi

# Create required directories
echo "Creating required directories and files"
mkdir -p "/data/web_static/releases/test/"
mkdir -p "/data/web_static/shared/"

# Create index.html file with test content
cat <<EOL > /data/web_static/releases/test/index.html
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
EOL

# Create symlink to /data/web_static/releases/test/ directory
ln -sf "/data/web_static/releases/test/" "/data/web_static/current"
echo "Symlink created: /data/web_static/current -> /data/web_static/releases/test/"

# Change ownership of data directory and files
chown -hR ubuntu:ubuntu /data/

# Updating nginx configuration to serve specified directory
echo "Editing config file"
cat <<EOL >> /etc/nginx/nginx.conf
http {
  server {
    location /hbnb_static {
      alias /data/web_static/current/;
      autoindex off;
    }
  }
}
EOL

# Restarting nginx service
if nginx -t; then
	service nginx restart
else
	echo "Please re-check configuration file"
fi
