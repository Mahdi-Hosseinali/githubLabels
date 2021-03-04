# Summary

This is a simple python file to manage the labels of a github repository.
The labels can be either saved from a repository to a json file or loaded from a json file to a repository.

# Use
The get the labels from public repository `https://github.com/octocat/Hello-World` to a file named `hello-world-labels.json`, call

```python github_labels.py -f hello-world-labels.json -u octocat -r Hellow-World```

If the repository was private, then `-t 381someSampleTokenHere3241` or `-p octaCatPassword` could be added to the command for authentication.

After a json file is available, then the labels of a repository can be set by calling a second command

`python github_labels.py -f github-labels.json -u Mahdi-Hosseinali -r repo-name -a set -t 381someSampleTokenHere3241`

# Credit
The current json file is taken from [here](https://github.com/abdonrd/github-labels)

# Requirements
The code is written in python 3.8.3 but should work with anything above 3.6 that supports f strings.
The only requirement is the `requests` library.