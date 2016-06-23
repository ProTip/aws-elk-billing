#This script modify the Default visualizations for checking the persistance in the other test script 'check_add_del_modify.sh'
#check there must not exist visualization Total_BlendedCost
CONTENT=`curl -XGET "http://elasticsearch:9200/.kibana/visualization/Total_BlendedCost"`;
if [[ $CONTENT == *'"found":true'* ]]
then
    echo 'Total_BlendedCost visualization exists, something is wrong... aborting'
    exit 1;
fi
echo 'Total_BlendedCost visualization doesnt exist, will create it...'

#create new visualization Tolal_BlendedCost
CREATE_VIS=$(curl -XPUT "http://elasticsearch:9200/.kibana/visualization/Total_BlendedCost" -d "`cat test/scripts/Total_BlendedCost.json`");
#delete default visualization Total_UnblendedCost
DELETE_VIS=`curl -XDELETE "http://elasticsearch:9200/.kibana/visualization/Total_UnblendedCost"`;

