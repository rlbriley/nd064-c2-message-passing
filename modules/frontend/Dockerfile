FROM node:14.8.0-alpine3.12

WORKDIR /app

COPY /modules/frontend/package.json /app
COPY /modules/frontend/package-lock.json /app

RUN npm install
RUN npm install react-scripts@3.4.3 -g

COPY /modules/frontend/ /app

EXPOSE 3000

CMD ["npm", "start"]

