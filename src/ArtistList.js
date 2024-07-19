
import React from "react";
import * as func from './functions.js';
import { Link} from "react-router-dom";

export default function Artist({artist}){
    let daArtist = func.listArtists(artist)
    let image = func.image(artist)
    let data = {...artist}
    return(
        
        <div className="container-search-result">
        {/* //<div> */}
            {/* // <div onclick ={handleClick}> */}
            {/* <div className="search-result-picture"> */}
            <div class = "artist-div">
                {/* <img src= {`${image}`}></img> */}
            {/* </div>
            <div className="artist-text"> */}
            <Link to= "/ArtistPage" state= {{data: data}}>
                <h1 class="center"><img class = "middle" src= {`${image}`} width={150} height={150}/>{daArtist}</h1>
            </Link>
            </div>
            
            
        </div>
        
    )
}