#!/usr/bin/env python
#
# Author: bear (Mike Taylor)
# License: MIT
# Copyright (c) 2014-2015 by Mike Taylor
#

from __future__ import print_function

import os, sys
import json
import datetime
import argparse

from github import Github
from bearlib.config import Config


def getUser(o):
    result = {}
    if o is not None:
        result['login'] = o.login
        result['name']  = o.name
        result['id']    = o.id
    return result

def getDate(d):
    if d is None:
        return ""
    else:
        return datetime.datetime.strftime(d, "%Y%m%dT%H%M%SZ")

def getMilestone(o):
    result = {}
    if o is not None:
        result["id"]          = o.id
        result["state"]       = o.state
        result["number"]      = o.number
        result["description"] = o.description
        result["title"]       = o.title
        result["due_on"]      = getDate(o.due_on)
        result["created_at"]  = getDate(o.created_at)
        result["updated_at"]  = getDate(o.updated_at)
    return result

def getComment(o):
    result = {}
    if o is not None:
        result['id']         = o.id
        result['body']       = o.body
        result['user']       = getUser(o.user)
        result['created_at'] = getDate(o.created_at)
        result['updated_at'] = getDate(o.updated_at)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', default='./archive.cfg')
    parser.add_argument('-i', '--issues', action='store_true')
    parser.add_argument('-o', '--org')
    parser.add_argument('-r', '--repo')

    args = parser.parse_args()
    cfg  = Config()
    cfg.fromJson(args.config)

    if cfg.auth_token is None:
        error('Unable to load configuration file %s' % args.config)
    else:
        gh = Github(cfg.auth_token)
        org = gh.get_organization(args.org)
        repo = org.get_repo(args.repo)

        if repo is not None:
            print('scanning', repo.name)
            data = {}
            if args.issues:
                data['issues'] = []
                for issue in repo.get_issues(state="all"):
                    i = { "id":         issue.id,
                          "state":      issue.state,
                          "body":       issue.body,
                          "number":     issue.number,
                          "repo":       repo.name,
                          "assignee":   getUser(issue.assignee),
                          "user":       getUser(issue.user),
                          "milestone":  getMilestone(issue.milestone),
                          "closed_at":  getDate(issue.closed_at),
                          "closed_by":  getUser(issue.closed_by),
                          "title":      issue.title,
                          "url":        issue.url,
                          "created_at": getDate(issue.created_at),
                          "labels":     [],
                          "comments":   [],
                        }
                    for comment in issue.get_comments():
                        i['comments'].append(getComment(comment))
                    for label in issue.labels:
                        i['labels'].append(label.name)
                    data['issues'].append(i)

                print('\t', len(data['issues']), 'issues')

            with open('%s.json' % repo.name, 'w+') as h:
                h.write(json.dumps(data, indent=2))

