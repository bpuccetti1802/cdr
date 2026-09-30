# Step 1: Build the Angular application
FROM node:20.18-alpine AS build
WORKDIR /app

# Proxy settings
ENV http_proxy=http://10.173.21.20:3128 
ENV https_proxy=http://10.173.21.20:3128
 
COPY .npmrc ./
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build 

# buildo le story
RUN npm run build-storybook 

# Step 2: Serve l'applicazione con NGINX
FROM nginx:alpine

RUN rm /etc/nginx/conf.d/default.conf
# Copia il template del file di configurazione NGINX
COPY nginx.conf.template /etc/nginx/templates/nginx.conf.template

# Copia l'app Angular costruita nella directory NGINX
COPY --from=build /app/dist/mf-shared-library /usr/share/nginx/html

# Copia build Storybook
COPY --from=build /app/storybook-static /usr/share/nginx/html/storybook

# Imposta le variabili d'ambiente (puoi passarle anche al runtime)
ENV nginxPort=4201
ENV hostName=localhost
ENV host=4200

# Sostituisci le variabili nel file di configurazione NGINX usando envsubst
RUN envsubst '\$nginxPort \$hostName \$host' < /etc/nginx/templates/nginx.conf.template > /etc/nginx/conf.d/default.conf

EXPOSE 4201

CMD ["nginx", "-g", "daemon off;"]
