## List Ec2

This script list all Ec2 server of a given region andreturn some information like ec2 type, private and public IP, ebs size, status.  

### Usage

This script has been tested with python 3.8.

## Prerequisites

##### Linux/Mac OS
```
python 3.8
```

##### Installing

```
$ git clone git@github.com:adrianocanofre/ec2-list.git
$ cd ec2-list
$ pip3  install -r requirements.txt
```

## Configure

Is possible to usage some environments variables such as `EC2_AWS_PROFILE` and `EC2_AWS_REGION`.

Example
``` 
export EC2_AWS_PROFILE=development
export EC2_AWS_REGION=us-east-1
``` 
If no variables set, default values will be used.(`EC2_AWS_PROFILE=default`, `EC2_AWS_REGION=eu-central-1`)


## Running the script
Basic run:

``` 
$ python ec2.py

$ python ec2.py -n 'test' 

$ python ec2.py -n '*test*'

$ python ec2.py -n '*test*' -s ASC 

```
