
export async function fileReader(){
    //let idJson = []
    let idJson = []
    for(let i = 0; i < 5; i++){
        const url = `https://raw.githubusercontent.com/jangablox/spotFiles/master/idCluster${i}.txt`
        const response = await fetch(url);
        const data = await response.text();
        const dataParsed = JSON.parse(data)
        idJson.push(dataParsed)
    }
    idJson = {
        ...idJson[0],
        ...idJson[1],
        ...idJson[2],
        ...idJson[3],
        ...idJson[4]
    }
    
    return idJson; 
}


export async function getClusterGroup()
{
    let clusterGroup = [];

    for(let i = 0; i < 10; i++){
        const url = `https://raw.githubusercontent.com/jangablox/spotFiles/master/cluster${i}.txt`
        const response = await fetch(url);
        const data = await response.text();
        clusterGroup.push(data.split('\n'))
    }

    return clusterGroup;
}





export async function getToken(){
    const CLIENTID = '859fceebd0da48b7b9a7967a6c7cf932'
    const CLIENTSECRET = 'a2066e3c1904449a971dfa4203659ffc'

    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': `Basic ${btoa(CLIENTID + ':' + CLIENTSECRET)}` },
        body: 'grant_type=client_credentials'
    };
    
    const response = await fetch('https://accounts.spotify.com/api/token', requestOptions);
    let data = await response.json();
    return data.access_token    
    
   
}



function cosineSimilarity(v1, v2){
    let dot = 0;
    let mag1 = 0;
    let mag2 = 0;
    for(let metric in v1){
        if (!(metric == 'id'|| metric == 'popularity' || metric == 'cluster')){
            dot += (v1[metric] * v2[metric]);
            mag1 += (v1[metric] * v1[metric]);
            mag2 += (v2[metric] * v2[metric]);
        }
    }
    mag1 = Math.sqrt(mag1);
    mag2 = Math.sqrt(mag2);
    return dot/ (mag1 * mag2);

}

export async function getSimilar(id, popLvl, idJson, clusterGroup, popZones){
   
    let cluster = idJson[id]['Cluster']
    let v1 = idJson[id]
    let searchStart = popZones[cluster][popLvl]
    let searchEnd = popZones[cluster][popLvl + 1]
    let similar = [[-1,""],[-1,""],[-1,""],[-1,""],[-1,""]]
    let smallest = -1
    for(let i = searchStart; i < searchEnd; i++){
        if(clusterGroup[cluster][i] != id){
            // console.log(clusterGroup[cluster][i])
            let cosSim = cosineSimilarity(v1, idJson[clusterGroup[cluster][i]])
            
            if( cosSim > smallest){
                let newSmallest = similar[0][0]
                for(let j = 0; j < 5;j++){
                    if(similar[j][0] == smallest){
                        similar[j][0] = cosSim
                        similar[j][1] = clusterGroup[cluster][i]
                        break;
                    }
                }
                for(let j = 0; j < 5; j++){
                    if(similar[j][0] < newSmallest){
                        newSmallest = similar[j][0]
                    }
                }
                smallest = newSmallest

            }
                    
            
        }
    }
    return [similar[0][1], similar[1][1], similar[2][1], similar[3][1], similar[4][1]]
}   

let searchArr = [];

export async function search(char, accessToken, idJson, pop){
    
    
    const requestOptions = {
        method: 'GET',
        headers: { 'Authorization': `Bearer ${accessToken}`},
    };
    const response = await fetch(`https://api.spotify.com/v1/search?q=${char}&type=artist&market=US&limit=5`, requestOptions);
    let data = await response.json();
    try{
        let items = data.artists.items
        let x = 5
        if(items.length < 5){
            x = items.length
        }
        searchArr = []
        for(let i = 0; i < x; i++){
            if(items[i].id in idJson){
                searchArr.push({'id':items[i].id, 'images':items[i].images[2].url, 'name':items[i].name, 'pop': pop})
            }
        }
        return searchArr
    }catch(error){
        return [{'name':''},{'name':''},{'name':''},{'name':''},{'name':''}]
    }
    
    


}



