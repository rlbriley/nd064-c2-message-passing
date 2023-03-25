FROM node:14.8.0-alpine3.12

WORKDIR /app

COPY /modules/app/frontend/package.json /app
COPY /modules/app/frontend/package-lock.json /app

RUN npm install
RUN npm install react-scripts@3.4.3 -g

CMD ["pwd"]

COPY /modules/app/frontend/ /app

EXPOSE 3000

CMD ["npm", "start"]

