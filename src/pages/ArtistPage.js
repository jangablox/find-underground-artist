import React,{useState, useEffect} from "react";
import { useLocation } from "react-router-dom";
import * as af from '../allFunc.js'
import SimArtist from './SimArtist.js'


let idJson = await af.fileReader()
let clusters = await af.getClusterGroup()
let accessToken = await af.getToken()
const popZones = [[0,5,555,1962,2702], [0,24,1425,4132,5200], [0,12,1008,3190,4152],[0,50,1905,5317,6249],[0,5,423,2033,3032],[0,5,434,1830,2381],[0,5,392,1199,1477],[0,22,1197,3718,4478],[0,11,1541,4542,5536],[0,15,1219,3405,4248]]
// async function setArtist_(id, pop, idJson, clusters, popZones){
//     return await af.getSimilar(id, pop, idJson, clusters, popZones)
// }
function ArtistPage(props){
    const [artists, setArtist] = useState([])
    const location = useLocation()
    const data = location.state?.data
    let image = data.images
    const fetchData = async() =>{
        let artists = await af.getSimilar(data.id, Math.abs(data.pop - 3), idJson, clusters, popZones)
        let temp = []
        for(let i = 0; i < artists.length;i++){
            const requestOptions = {
                method: 'GET',
                headers: { 'Authorization': `Bearer ${accessToken}`},
            };
            const response = await fetch(`https://api.spotify.com/v1/artists/${artists[i]}`, requestOptions);
            let data = await response.json();
            temp.push({'id':data.id, 'images':data.images[2].url, 'name':data.name})

        }
        artists = temp
        return artists
        
    }
    useEffect(() =>{
        fetchData().then((res) =>{
            setArtist(res)
        })
    },[])
    // setArtist(data.id, data.pop - 1, idJson, clusters, popZones)
    
    return(
        <>
        <div className="Bigg">
        <h1 className="Bigg1"><img class="middle" src= {`${image}`} width={200} height={200}></img> Results for {data.name}</h1>
            
            
        </div>
        <br></br>
        <SimArtist artist = { artists[0]} />
        <br></br>
        <SimArtist artist = { artists[1]} />
        <br></br>
        <SimArtist artist = { artists[2]} />
        <br></br>
        <SimArtist artist = { artists[3]} />
        <br></br>
        <SimArtist artist = { artists[4]}/>
         </>
    )
}

export default ArtistPage