# github-archive

Create a tarball of the cloned repo and all issues

Assumes that /tmp/ is writable and will create an /tmp/archive directory to store the tarball.

After creating a personal access token on https://github.com/settings/tokens
and copying it to archive.cfg archive a repo using this command:

    ./archive.sh orgname reponame


## Requirements

- Python v2.7+
- pip install bearlib  (https://github.com/bear/bearlib)
- pip install PyGithub (https://github.com/PyGithub/PyGithub)

## Using it
Make sure
