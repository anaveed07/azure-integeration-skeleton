#!/bin/bash
echo "----Run vncserver"
USER=$USER
HOME=$HOME
export USER HOME
echo "vmCloud63012\nvmCloud63012\ny"| vncserver
