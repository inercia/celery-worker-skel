#!/bin/sh

PREFIX=$1

if [ -d $PREFIX/.hg ] ; then
    cd $PREFIX && echo $(hg summary | grep parent | cut -d ':' -f 2 | sed -e 's/\ //g')
elif [ -d $PREFIX/.git ] ; then
    cd $PREFIX && echo $(git log --oneline | wc -l)
    #FULL_REL=$(git describe --all --abbrev=4 HEAD^ | sed -e 's/tags\///g')
    #REL=$(echo $FULL_REL | sed -s 's/-/\ /g' | awk '{ print $3 }')
    #echo $REL
else
    echo ''
fi
