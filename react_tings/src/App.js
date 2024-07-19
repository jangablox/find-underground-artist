import Artist from './ArtistList';
import React, {useState, useRef} from 'react';
import * as af from './allFunc.js'
import './index.css'


let idJson = await af.fileReader()
let accessToken = await af.getToken()

function App() {

  // const [artists, setArtist] = useState(['','',''])
  const[artists, artistSet] = useState([{'name':''},{'name':''},{'name':''},{'name':''},{'name':''}])
  const[pop, popSet] = useState(1)
  const artistNameRef = useRef()
  let currSearch = null
  const nonoWords = new Set(['Enter', 'CapsLock', 'Alt','Control','Shift','Tab'])


  async function handleArtistSearch(e){
    
    let key = e.key
    if(nonoWords.has(key)){
      currSearch = artistNameRef.current.value
      
    }
    else if(key === 'Backspace'){
      currSearch = artistNameRef.current.value.slice(0,-1)
    }
    else{
      currSearch = artistNameRef.current.value + key
    }
    
    let searchResults
    if(artistNameRef.current.value === ''){
      searchResults = [{'name':''},{'name':''},{'name':''},{'name':''},{'name':''}]
    }
    else{
      searchResults = await af.search(currSearch,accessToken,idJson,pop)
    }
    
    artistSet(arg => {
      // if(key === 'Enter'){
      //   artistNameRef.current.value = null
      //   return searchResults
      // }
      return searchResults
    });
    

  }

  async function handlePopChange(e){
    
    popSet(arg =>{
      return e.target.value
    });
  }


  return (
    <>
        <div className='pop-Button'>
          <div className="slider-container">
              <div className="range-fill"></div>	
              <input className='slider' type="range" min="0" max="3" defaultValue={1} id="fader" onChange = {handlePopChange}></input>
          </div>
        
          <div className="label-container">
              <div className="label">Upcoming</div>
              <div className="label">Underground</div>
              <div className="label">Main Stream</div>
              <div className="label">Super Star</div>
          </div>
      </div>
    
      <div class = "container-logo">

        <img className = "logo" src = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSbEq-U-qfopzP9STZ1c7vYvy662Hxu2h5Py94JiFiP&s"></img>
      </div>
      <h2 className = "title-text">Find Artists based on Music Taste and Popularity</h2>
      <div className = "container-search-bar">
        <form className='search-bar'>

          <input ref = {artistNameRef} type = 'text' onKeyUp={handleArtistSearch} placeholder='Search Artists'></input>
         
          
        </form>
        
      </div>
      <br></br>
      <Artist artist = { artists[0]} />
      <br></br>
      <Artist artist = { artists[1]} />
      <br></br>
      <Artist artist = { artists[2]} />
      <br></br>
      <Artist artist = { artists[3]} />
      <br></br>
      <Artist artist = { artists[4]}/>
      <br></br>
      
      <br></br>
      
    </>
    

  );
}

export default App;
