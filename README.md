# Restaurant lunch selection management application

The intention of the application is to help restaurant employees make decisions which menu to choose for today. 
Basically two roles are presented:
* Administrator
* Worker

Administrators are in charge of: 
* Opening new restaurants.
* Hiring new employees.

Each employee with Worker role is assigned to one restaurant and might do the following:
* Uploading a new menu.
* Voting for the menus uploaded today.
* Seeing the current chosen menu. It is selected by maximum number of words.
* Seeing all the uploaded menus ranked by the given votes.

Note: an employee with worker role allowed to perform the tasks specified above only in restaurant he works for.

Administrators do not have a restaurant assigned to them.
Also, they do not allowed uploading and voting for menus, seeing voted results and chosen menu.  


## Install

Change the current directory to src being at the root directory and run the following command
```
make up
```

## Uinstall

Being at the src directory run the following command:
```
make wipe
```

## Running test and linter checker
```
make run_checks
```

## API Documentation
[Swagger documentanion](http://localhost:8000/swagger/)

## Authentification

For the convenience purposes predefined user exists with administrator role.
To get an access to API Bearer token has to be acquired.
This can be done throughout API described at swagger docs.
```
login: admin
password: Ol4iZsa=
```
