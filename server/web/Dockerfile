FROM node
EXPOSE 3000
CMD npm run serve

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY . .
