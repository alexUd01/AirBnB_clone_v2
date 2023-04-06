#!/usr/bin/env bash
# Write a Bash script that sets up your web servers for the deployment of
# web_static.

# It must:
#     1 Install Nginx if it not already installed
#     2 Create the folder /data/ if it doesn’t already exist
#     3 Create the folder /data/web_static/ if it doesn’t already exist
#     4 Create the folder /data/web_static/releases/ if it doesn’t already exist
#     5 Create the folder /data/web_static/shared/ if it doesn’t already exist
#     6 Create the folder /data/web_static/releases/test/ if it doesn’t already exist
#     7 Create a fake HTML file /data/web_static/releases/test/index.html (with
#       simple content, to test your Nginx configuration)
#     8 Create a symbolic link /data/web_static/current linked to
#       the /data/web_static/releases/test/ folder. If the symbolic link already
#       exists, it should be deleted and recreated every time the script is ran.
#     9 Give ownership of the /data/ folder to the ubuntu user AND group (you
#       can assume this user and group exist). This should be recursive;
#       everything inside should be created/owned by this user/group.
#     10 Update the Nginx configuration to serve the content
#        of /data/web_static/current/ to hbnb_static (ex: https://mydomainname.tech/hbnb_static).

# Don’t forget to restart Nginx after updating the configuration:
# Use alias inside your Nginx configuration
# Your program should always exit successfully. Don’t forget to run your script
# on both of your web servers.

# Requirement 1
sudo apt-get update -y
sudo apt-get install nginx -y

sudo ufw allow 'Nginx HTTP'

# Requirement 2, 3, 4, 5, 6, 9
sudo mkdir -p /data/web_static/{releases/test,shared}  # Cheers
sudo chown -R "ubuntu":"ubuntu" /data

# Requirement 7
sudo echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Requirement 8
sudo rm -rf /data/web_static/current
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Requirement 10
old_str="\tlisten 80 default_server;"
# forward slashes are escaped to prevent sed from marking it as the end of replacement string.
replacement_str="$old_str\n\n\tlocation \/hbnb_static\/ {\n\t\talias \/data\/web_static\/current\/;\n\t}"
sudo sed -i "s/$old_str/$replacement_str/" /etc/nginx/sites-enabled/default

echo "Done"

sudo service nginx restart
