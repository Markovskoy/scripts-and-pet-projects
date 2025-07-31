#!/bin/bash
set -e

# === Backend ===
echo " Installing backend..."
cp /vagrant/backend/sausage-store*.jar /opt/sausage-store/bin/sausage-store.jar
chown -R backend:backend /opt/sausage-store

# === Frontend ===
echo " Installing frontend..."
cp -r /vagrant/frontend/* /opt/frontend/
chown -R www-data:www-data /opt/frontend

# === Systemd Unit ===
echo " Setting up systemd unit for backend..."
cp /vagrant/systemd/backend.service /etc/systemd/system/backend.service

# === Nginx config ===
echo " Configuring Nginx..."
cat <<EOF > /etc/nginx/sites-available/frontend
server {
    listen 80;
    server_name localhost;

    root /opt/frontend;
    index index.html;

    location / {
        try_files \$uri \$uri/ =404;
    }

    location /api/ {
        proxy_pass http://localhost:8080/api/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

ln -sf /etc/nginx/sites-available/frontend /etc/nginx/sites-enabled/frontend
rm -f /etc/nginx/sites-enabled/default

# === Firewall ===
iptables -A INPUT -m tcp --dport 8080 -p tcp -j ACCEPT
iptables -A INPUT -m tcp --dport 80 -p tcp -j ACCEPT

# === Запуск сервисов ===
systemctl daemon-reexec
systemctl enable backend.service
systemctl restart backend.service
systemctl restart nginx

echo " Setup completed."
