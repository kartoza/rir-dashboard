# Development environment

## How to setup development environment
This section is for setup development so we can develop the project and check the changes in runtime.


## Using pycharm
This section is for using pycharm.
Requirement: 
- Pycharm
- Finished **Setting up the project**

### Setup interpreter
1. Go to file -> setting -> Project -> Project Interpreter -> click cog -> add
<br>![Project Interpreter ](../../img/development-setup/1.png "Project Interpreter")<br><br>

2. Go to ssh interpreter -> Fill the form like below
<br>![Project Interpreter ](../../img/development-setup/2.png "Project Interpreter")<br><br>

3. Click next and fill **docker** as password
<br>![Project Interpreter ](../../img/development-setup/3.png "Project Interpreter")<br><br>

4. Click next and change interpreter like below and click finish
<br>![Project Interpreter ](../../img/development-setup/4.png "Project Interpreter")<br><br>

5. After finish, it will show all package like below.
<br>![Project Interpreter ](../../img/development-setup/5.png "Project Interpreter")<br><br>

6. In current page, click **path mappings**, click + button and put local path to where the project (django-project folder) and remote path is like below. and click oK.
<br>![Project Interpreter ](../../img/development-setup/6.png "Project Interpreter")

Now the interpreter is done. When we restart the machine, we need to do `make up` to run the project.

### Setup run configuration
After the interpreter is done, we need configuration to run the project in development mode.

1. Click "Add configuration" like in the cursor in the image below. (top-right)
<br>![Project Interpreter ](../../img/development-setup/7.png "Project Interpreter")<br><br>

2. There will be a popup, and click +, then click **django server** like below
<br>![Project Interpreter ](../../img/development-setup/8.png "Project Interpreter")
<br>![Project Interpreter ](../../img/development-setup/9.png "Project Interpreter")<br><br>

3. It will show the form and fill like below. 
<br>![Project Interpreter ](../../img/development-setup/10.png "Project Interpreter")<br><br>

4. Don't click the OK yet, but click **Environment Variables** and add environments like below 9by clicking + button).
<br>![Project Interpreter ](../../img/development-setup/11.png "Project Interpreter")<br><br>

5. After that, click OK.

6. Now we need to run the server by clicking **go** button in below image.
<br>![Project Interpreter ](../../img/development-setup/12.png "Project Interpreter")<br><br>

7. When we click the **go** button, pycharm will run a process until like image below.
<br>![Project Interpreter ](../../img/development-setup/13.png "Project Interpreter")<br><br>

8. Now it is done. We can access the development server in [http://localhost:2000/](http://localhost:2000/)

This development mode is DEBUG mode, and also whenever we change the code, the site will also change in runtime.

Now it is ready to be developed.
For more information how to install docker, please visit [Using a Docker Compose-Based Python Interpreter in PyCharm](https://kartoza.com/en/blog/using-docker-compose-based-python-interpreter-in-pycharm/)


