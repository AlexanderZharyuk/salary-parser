# SALARY PARSER

Scripts for obtaining information on salaries at labor exchanges.

The analysis is taken from the sites: [HeadHunter](https://hh.ru/) and [SuperJob](https://www.superjob.ru/) by API.


## Setting up your development environment
1. Install the required libraries:
To do this, use the command:
```shell
pip install -r requirements.txt
```
2. Set up `.env` -file:
Inside this file there should be a variable with your secret key from the SuperJob API:
```
SUPERJOB_SECRET_KEY=<YOUR-SECRET-KEY>
```

## Running scripts
If you want to display data for two sites at once, use the command:
```shell
python3 main.py
```
This script will start collecting information on sites and at the end will issue a table like this:

![Screenshot 2022-07-13 at 17 11 55](https://user-images.githubusercontent.com/103115934/178754677-2d17d496-2f11-4b73-84b8-545e01b036c0.png)

While the script is running, you will see the progress of the work, so that you understand that the script is still executing and at what stage it is:

![Screenshot 2022-07-13 at 17 14 08](https://user-images.githubusercontent.com/103115934/178755205-6a76f432-055a-4464-a911-e83a2b8da245.png)

If you are interested in the table only for a specific site, use the following commands:

For **HH**:
```shell
python3 hh.py
```

For **SuperJob**:
```shell
python3 superjob.py
```

At this stage, the script is looking for information only in Moscow.

## Created with
* [HH](https://hh.ru/) - Website with vacancies
* [SuperJob](https://www.superjob.ru/) - Site with vacancies

## Author
[Alexander Zharyuk](https://github.com/AlexanderZharyuk/)

## Feature for the next update
- [ ] Add a config in which:
1. The user will be able to choose the id of the city, without fixing the code
2. The user can use their own keywords to search
