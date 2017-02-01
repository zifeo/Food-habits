## 1. Installation of necessary tools
Install **git** version control system
> <https://git-scm.com/downloads>

## 2. Pull the project TODO MODIFY
You can simply clone the project locally by using the command:
```bash
git clone https://github.com/sdfepfl/javascript-boilerplate.git
cd javascript-boilerplate
```

## 3. Run the installation script TODO MODIFY
The installation script will take care of installing [NodeJS](https://nodejs.org), as well as setting everything up: 

```bash
./install_server.sh
```

Specifically, it'll install NodeJS dependencies required to run the app in a folder named `node_modules`.

## 4. start command

Most common command, run the app in development mode (calls `nodemon` under the hood):
```bash
npm start
```

the app will be run and available at:
> <http://localhost:3000>

## 5. Small visualization using the elastic search database we created.
You can search for dishes in the trend field to show which restaurants have it in one of their meals.

We use it to show how some dishes are present only in some regions.

Some easy examples :
- Fondue au fromage, fondue savoyarde
- Malakoff, choucroute