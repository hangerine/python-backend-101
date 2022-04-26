## Book Information
----
title: '깔끔한 파이썬 탄탄한 백엔드' <br/>
author: '송은우' <br/>
email: 'songew@gmail.com' <br/>
publisher: 'BJPUBLIC' <br/>
print date: '25Jan2019' <br/>
github: 'https://github.com/rampart81/python-backend-book' <br/>

## AWS Information
----
login: hangjun.min@gmail.com <br/>
root user: Lu*******@ <br/>
EC2 instances: 
```json
[
    {
        "public_ip": "15.164.218.248",
        "private_dns": "ip-172-31-32-159.ap-northeast-2.compute.internal",
        "type": "t2.micro",
        "key_pair_name": "python-backend",
        "pem": "python-backend.pem",
        "ssh": "sudo ssh -i ~/Download/python-backend.pem ubuntu@15.164.218.248",
        "security_rules": {
            "inbound": {
                "port": "22,5000"
            },
            "outbound": {
                "port": "*"
            }
        },
        "storage": "12GB",
        "AMI": "Ubuntu 18.04"
    },
    {
        "public_ip": "13.209.26.140",
        "private_dns": "ip-172-31-46-155.ap-northeast-2.compute.internal",
        "type": "t2.micro",
        "key_pair_name": "python-backend",
        "pem": "python-backend.pem",
        "ssh": "sudo ssh -i ~/Download/python-backend.pem ubuntu@13.209.26.140",
        "security_rules": {
            "inbound": {
                "port": "22,5000"
            },
            "outbound": {
                "port": "*"
            }
        },
        "storage": "12GB",
        "AMI": "Ubuntu 18.04"
    }
]
```
S3 instances: 
```json
[
    {
        "name": "python-backend-s3",
        "arn": "arn:aws:s3:::python-backend-s3",
        "bucket_url": "http://python-backend-s3.s3.amazonaws.com/",
        "bucket_policy": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "Stmt1544434281506",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": "arn:aws:s3:::python-backend-s3/*"
                }
            ]
        },
        "cors": [
            {
                "AllowedHeaders": [
                    "*"
                ],
                "AllowedMethods": [
                    "GET"
                ],
                "AllowedOrigins": [
                    "*"
                ],
                "ExposeHeaders": [],
                "MaxAgeSeconds": 3000
            }
        ]
    }
]
```
IAM: 
```json
{
    "name": "python-backend-s3",
    "permissions": "AmazonS3FullAccess",
    "access_key": "AKIARCGL4HLSVSPTZI5F",
    "secret_key": "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",
}
```
ALB:
```json
{
    "name": "python-backend-alb",
    "dns": "python-backend-alb-2054143807.ap-northeast-2.elb.amazonaws.com",
    "ip_type": "ipv4",
    "AZ": [
        "ap-northease-2a",
        "ap-northease-2b",
        "ap-northease-2c",
        "ap-northease-2d"
    ],
    "security_group": {
        "name": "python-backend-alb",
        "inbound_rules": "80",
        "outbound_rules": "*"
    },
    "forwarding_to": "python-backend-target-group"
}
```
TargetGroups:
```json
{
    "name": "python-backend-target-group",
    "arn": "arn:aws:elasticloadbalancing:ap-northeast-2:073442015973:targetgroup/python-backend-target-group/5b5e1af69639ef2b",
    "port": "5000",
    "target": [
        "15.164.218.248",
        "13.209.26.140"
    ]
}
```
RDS:
```json
{
    "db_identifier": "database-1",
    "engine": "MySQL5.7.23",
    "size": "db.t3.micro",
    "endpoint": "database-1.ctlsetaj2jig.ap-northeast-2.rds.amazonaws.com",
    "port": "3306",
    "security_group": {
        "name": "MYSQL5.7",
        "inbound_rules": "3306",
        "outbound_rules": "*"
    },
    "parameter_group": {
        "character_set_client": "utf8mb4",
        "character_set_connection": "utf8mb4",
        "character_set_database": "utf8mb4",
        "character_set_results": "utf8mb4",
        "character_set_server": "utf8mb4",
        "collation_connection": "utf8mb4_general_ci",
        "collation_server": "utf8mb4_unicode_ci"
    },
    "username": "root",
    "password": "qwer1234",
    "mysql": "docker -it exec mysql mysql -h database-1.ctlsetaj2jig.ap-northeast-2.rds.amazonaws.com -u root -p"
}
```
RDS-Schema:
```sql
mysql> CREATE DATABASE miniter;
mysql> USE miniter;
mysql> CREATE TABLE users(
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    profile VARCHAR(2000) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY email (email)
);
mysql> CREATE TABLE users_follow_list(
    user_id INT NOT NULL,
    follow_user_id INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, follow_user_id),
    CONSTRAINT users_follow_list_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT users_follow_list_follow_user_id_fkey FOREIGN KEY (follow_user_id) REFERENCES users(id)
);
mysql> CREATE TABLE tweets(
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    tweet VARCHAR(300) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    CONSTRAINT tweets_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id)
);
mysql> show tables;
mysql> explain users;
mysql> ALTER TABLE users ADD COLUMN profile_picture VARCHAR(255);
```
## My Github Information
---
1. General Info
  - ID: hangerine
  - Email: hangjun.min@gmail.com
  - PassWord: Lu*******@
  - Personal Token (validate on 20.Jul.2022): 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
  - My github URL: https://github.com/hangerine
2. How to generate Personal Token
  - See https://geoseong.github.io/docs/scm/git/github-token-authentication/

## Configure Developement Env
---
### MacOS
install python3
> brew install python
install miniconda

Visit [Conda Hompage](https://conda.io/miniconda.html) and download miniconda script
> bash ./Miniconda3-latest-MacOSX-x86_64.sh
```bash
wget https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
conda list
conda create --name pyapi python=3.7
conda activate pyapi
conda deactivate pyapi
```

install git
> brew install git
```bash
git config --global user.name "hangjun.min"
git config --global user.email "hangjun.min@sk.com"
```
install text mode git
> brew install tig

install diff-so-fancy
> brew install diff-so-fancy
```bash
git config --global color.ui true

git config --global color.diff-highlight.oldNormal "red bold"
git config --global color.diff-highlight.oldHighlight "red bold 52"
git config --global color.diff-highlight.newNormal "green bold"
git config --global color.diff-highlight.newHighlight "green bold 22"

git config --global color.diff.meta "yellow"
git config --global color.diff.frag "magenta bold"
git config --global color.diff.commit "yellow bold"
git config --global color.diff.old "red bold"
git config --global color.diff.new "green bold"
git config --global color.diff.whitespace "red reverse"
```
install zsh
> brew install zsh zsh-completions

change shell
> sudo -s 'echo /usr/local/bin/zsh >> /etc/shells' && chsh -s /usr/local/bin/zsh

install Oh-my-zsh
> sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

config oh-my-zsh
```
#Path to your oh-my-zsh installation
export ZSH=$HOME/.oh-my-zsh

ZSH_THEME='agnoster'

plugins=(
    git
    osx
    autojump
    scala
    python
    pip
    github
    gnu-utils
    zsh-syntax-highlighting
    history-substring-search
    colored-man-pages
)
source $ZSH/oh-my-zhs.sh
source $(brew --prefix autoenv)/activate.sh
source /usr/local/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
# for miniconda
export PATH="/path/to/Miniconda3/bin:$PATH"
```

install httpie
> brew install httpie
```bash
http -v GET http://localhost:5000/ping
http -v POST http://locahost:5000/sign-up name=hangjun.min email=hangjun.min@sk.com password=test1234 profile="Christian. Software Engineer"
http -v POST localhost:5000/tweet id:=1 tweet="My first tweet"
http -v POST localhost:5000/follow id:=1 follow:=2
http -v GET localhost:5000/timeline/1
http -v POST localhost:5000/login email=hangjun.min@sk.com password=test1234
http -v POST locahost:5000/tweet tweet="hello world" "Authorization: Token..."
http -v --form localhost:5000/profile-picture profile_pic@/Users/hjmin/Pictures/acp_logo.png "Authorization: Token..."
http -v GET :5000/profile-picture/1
wget localhost:5000/profile-picture/1 -O profile.png
```

install mysql
> brew install mysql
```
mysql_secure_installation # set password
mysql.server start
mysql.server status
mysql.server stop

# Over 5.7 version
sudo mysql
SELECT user, plugin, host FROM mysql.user;
# change auth_socket to password
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
FLUSH PRIVILEGES;
SLECT user, authentication_string, plugin, host FROM mysql.user;
```
execute http.server
> python -m http.server

Github Code Commit
```bash
git init
git add .
git commit -m 'Initial Commit'
git remote add origin <remote repo URL>
git push -u origin master
```
Create sshkey
> ssh-keygen -t rsa -b 4096 -C "hangjun.min@sk.com"
```bash
cat ~/.ssh/id_rsa.pub
```
Virtual Env Freeze and Install
```bash
pip freeze > requirements.txt
pip install -r requirements.txt
```