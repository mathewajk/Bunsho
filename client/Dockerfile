# pull the official base image
FROM node:21

# set working directory
WORKDIR /usr/src/app

# add `/usr/src/app/node_modules/.bin` to $PATH
ENV PATH /usr/src/app/node_modules/.bin:$PATH
ENV HOST=0.0.0.0

# install and cache app dependencies
COPY package.json .
COPY package-lock.json .
RUN npm ci

# start app
CMD ["npm", "run", "dev"]
