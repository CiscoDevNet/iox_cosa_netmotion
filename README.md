# City of San Antonio - NetMotion IOx Integration

> If you are working on this project, please only work on one file at a time and please remember to checkout a branch before commiting and pushing code to this repo.

> The golang application in folder **iox-go** is currently being used.  The original python application is no longer being used.

## Getting Started

1. clone this Git repo to your computer `git clone https://github.com/CiscoDevNet/iox_cosa_netmotion`

2. Change directories to the correct folder you just cloned `cd iox_cosa_netmotion`.

3. Checkout a branch using the git checkout <branch_name> command. **example:** `git chechout gps_data`

4. work on the code for your branch and commit and push changes as needed.

## Build Docker Image

In the directory of iox_cosa_netmotion...

* Edit/Update code
* Build docker image
```bash
docker build -f Dockerfile.golang -t iox-cosa:v0.XX .
```


## Package IOx App

After building the docker image

```bash
ioxclient docker package --use-targz iox-cosa:v0.XX .
```

