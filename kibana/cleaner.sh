#!/bin/sh
docker ps | awk '/elk_/ { print $1 }' | while read doid; do
    docker inspect $doid | jq -r '.[]|{ LogPath }[], {Mounts }[][].Source' | while read dpath; do
        find $dpath -iname '*.log' -exec sh -c "echo > {}" \; -printf "Cleaned %p which had %s bytes \n"
    done
done
