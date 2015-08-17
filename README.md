![CoREdash Banner](https://raw.githubusercontent.com/alanplotko/CoREdash/master/static/assets/img/logo.png)

## About CoREdash

CoREdash is a web application that serves to enable members and alumni of Binghamton University's CoRE (Computers, Robotics, and Engineering) Living/Learning Community to stay in touch and organize events. CoRE is a Special Interest Housing option that consists of members who share interests in computers, robotics, and engineering.

## Usage

Just visit the website. CoRE embers can sign in with Google using their Binghamton University email address. After logging in, members can navigate and interact with the web application.

Note: For the duration of alpha development, access will only be given to CoRE members contributing to project development and testing.

## Technologies & Setup

CoREdash runs in Python 3 on Flask and MongoDB. You can checkout the modules in use in [requirements.txt](https://github.com/alanplotko/CoREdash/blob/master/requirements.txt). I particularly use Python 3.4.3.

After forking the project, create a virtual environment and install the requirements listed in the aforementioned file.

1) Install virtualenv if you have not already.

```
pip install virtualenv
```

2) Create a virtual environment in your project directory.

```
virtualenv venv
```

3) Activate the virtual environment.

```
source venv/bin/activate
```

4) Install requirements from requirements.txt

```
pip install -r /path/to/requirements.txt
```

5) Run CoREdash. I use an alias (python=python3) when working in a Linux environment. Be sure to appropriately modify these commands based on your environment (i.e. using python3 or pip3 where appropriate and so on).

```
python app.py
```

TODO: Discuss environment variables.

## Contributing

CoRE Members: fork it and feel free to submit a pull request! If you have any feature ideas, send me an email!

All others: this application is built for CoRE, but it can also be built to work for another organization, school or university club, and so on. Feel free to submit pull requests and contact me about improving CoREdash. The CoREdash name and corresponding logo belongs to CoRE. If you're using CoREdash to build your own application, please change the name and logo. The code is open-source and adheres to the included license.

## Changelog

Check out [CHANGELOG.md](https://github.com/alanplotko/CoREdash/blob/master/CHANGELOG.md) and commits for full details.

## License

Check out [LICENSE.md](https://github.com/alanplotko/CoREdash/blob/master/LICENSE.md) for full details. The CoREdash name and corresponding logo belongs to CoRE. If you're using CoREdash to build your own application, please change the name and logo. The code is open-source and adheres to the aforementioned license.
