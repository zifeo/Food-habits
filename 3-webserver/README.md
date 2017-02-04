# 3 webserver

As we had our data in the elastic search we decided to do a small visualization using leaflet to show food trends.

## Small visualization using the elastic search database we created.

You can search for dishes in the trend field to show which restaurants have it in one of their meals.

There is an instance running at this address 51.15.135.251:5000 (It will be shutdown in the beginning of the next semester)

We use it to show how some dishes are present only in some regions.

Some easy examples :
- Fondue au fromage, fondue savoyarde
- Malakoff, choucroute

## Installation

### Run the installation script (only on linux)

The installation script will take care of installing [NodeJS](https://nodejs.org), as well as setting everything up: 

```bash
./install_server.sh
```

Specifically, it'll install the NodeJS dependencies required to run the app in a folder named `node_modules`.

### build command

build the app for production:

```bash
npm run build:prod
```

### running the app on your computer

You can see the web app if you open the './public/index.html' file in your browser.