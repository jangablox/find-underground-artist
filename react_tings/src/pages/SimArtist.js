import React from "react";
import * as func from '../functions.js';



export default function SimArtist({artist}){
    console.log(artist)
    let daArtist = func.listArtists(artist)
    let image = func.image(artist)
    let data = {...artist}
    return(
        
        <div className="container-search-result">
            {/* // <div onclick ={handleClick}> */}
            {/* <div className="search-result-picture">
                <img src= {`${image}`}></img>
            </div>
            <div className="artist-text">
                <a href = {`https://open.spotify.com/artist/${data.id}`} target="_blank">
                    <h1>{daArtist}</h1>
                </a>
                </div> */}
            <a href = {`https://open.spotify.com/artist/${data.id}`} target="_blank">
            <h1 class="center"><img class = "middle" src= {`${image}`} width={150} height={150}/>{daArtist}</h1>
            </a>
        </div>
        
    )
}