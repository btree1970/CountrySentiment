import USAMAP from 'react-usa-map'
import React, { Component } from 'react'
import ReactDOM from 'react-dom'

import * as utils from './utils'

class App extends Component {

     constructor(props) {
         super(props)
          
         this.state = {senitmentID: 0, sentimentObj: {} }
         this.onStateClickHandler = this.onStateClickHandler.bind(this)
         this.getHexColor = this.getHexColor.bind(this)
     }

     mapHandler = (event) => {
        alert('how are you doing')
     };

    //  {
    //   "NJ": {
    //     fill: "navy",
    //     clickHandler: this.onStateClickHandler()
    //   },
    //   "NY": {
    //     fill: "#CC0000"
    //   }
    // };

    onStateClickHandler = (event) => {
    }

     getHexColor = (value) => {
        return utils.getColorGradient(value)
     }

     statesCustomConfig = () => { 
        let  stateMapObject = {}
        for (var key in this.state.sentimentObj) {
            let fill = this.getHexColor(this.state.sentimentObj[key])
            stateMapObject[key] =
              {
                fill: fill,
                clickHandler: this.onStateClickHandler()   
            }
        }
        return stateMapObject
      };

    componentWillMount =  () => {
           fetch('http://localhost:8080/api/score').then((response) => {
               return response.json()
           }).catch((error) => {
               console.log(error)
           }).then((data) => { 
               this.setState({sentimentObj: data})
           })
    }
     render() {
        let divergingScheme = ["#93003a", "#ae1045", "#c52a52", "#d84360", "#e75d6f", "#f4777f", "#fd9291", "#ffaea5", "#ffcab9", "#ffe5cc", "#efec6b", "#deda5a", "#cac94b", "#b4b93e", "#9da932", "#849a26", "#6b8c1c", "#507e11", "#326f07", "#006100"]


        return (
            <div className="App">
                <div className="title">
                    Hello
                </div>

                
                <div className="popularTags">
                      
                </div>
                <div className="map">
                   <USAMAP  customize={this.statesCustomConfig()} /> 
                </div>
                <div className="colorScheme">
                      <div className="legend">
                        <h3>Negative</h3>
                        <h3>Positive</h3>
                        </div>
                    <div className="colormap">
                        {divergingScheme.map((key, value) => {
                            return <div className='colormapItem' style={{backgroundColor: `${key}`}} id={`${key}-index`} ></div>
                        })}
                    </div>
                </div>
            </div>
        )
     }
}

ReactDOM.render(
  <App/>,
  document.getElementById('main')
);

