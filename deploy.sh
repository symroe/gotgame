#!/bin/bash

cd scripts && fab $1 git_export && fab $1 deploy
