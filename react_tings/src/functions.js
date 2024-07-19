
export function listArtists(artists){
    if(artists === undefined){
        return ""
    }
    return artists['name']
}

export function searchArtist(currSearch){
    return [currSearch, 'Saba', 'laufey']
}

export function image(artist){
    if(artist === undefined){
        return 'https://images.squarespace-cdn.com/content/v1/58f56c10d2b857170c9ac044/1519534019246-BTNF5DSIPKUZD7FB5VY6/Black+Square'
    }
    if(artist.images === undefined){
        return 'https://images.squarespace-cdn.com/content/v1/58f56c10d2b857170c9ac044/1519534019246-BTNF5DSIPKUZD7FB5VY6/Black+Square'
    }
    return artist.images
}

// export async function setArtist(){
//     return await af.getSimilar(data.id, data.pop - 1, idJson, clusters, popZones)
// }