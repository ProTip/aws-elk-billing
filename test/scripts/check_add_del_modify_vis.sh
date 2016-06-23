#This scripts check the persistance of the modification made by test script 'add_del_modify_vis.sh'
#check if the default visualization Total_UnblendedCost recreated or not
CONTENT=`curl -XGET "http://elasticsearch:9200/.kibana/visualization/Total_UnblendedCost"`;
if [[ $CONTENT == *'"found":false'* ]]
then
    echo 'The default visualization Total_UnblendedCost could not be recreated, test unsuccessful :('
	exit 1;
fi
echo 'The default visualization Total_UnblendedCost recreated, test success :)'

#check if the newly created visualization Total_BlendedCost persists or not
CONTENT=`curl -XGET "http://elasticsearch:9200/.kibana/visualization/Total_BlendedCost"`;
if [[ $CONTENT == *'"found":false'* ]]
then
    echo 'The newly created visualization Total_BlendedCost did not persist, test unsuccessful :('
    exit 1;
fi
echo 'The newly created visualization Total_BlendedCost persists, test success :)'

#delete the all index to make sure local teardown takes place
DELETE_INDEX=`curl -XDELETE "http://elasticsearch:9200/*"`
exit 0;
