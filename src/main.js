import USAMAP from 'react-usa-map'
import React, { Component } from 'react'
import ReactDOM from 'react-dom'

import * as utils from './utils'

const buttonBackground = '#ffffff'
const clickedButtonBackground = '#f6b93b'

class App extends Component {

     constructor(props) {
         super(props)
          
         this.state = {
             senitmentID: 0,
             sentimentObj: {},
             topics: {},
            }

         this.onStateClickHandler = this.onStateClickHandler.bind(this)
         this.getHexColor = this.getHexColor.bind(this)
         this.onButtonClickHandlerpopularTags = this.onButtonClickHandlerpopularTags.bind(this)
         this.fetchTopicHander = this.fetchTopicHander.bind(this)
     }

     mapHandler (event) {
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

    onButtonClickHandlerpopularTags (value)  {
        this.setState({senitmentID: value})

        //Load data topic
        this.fetchTopicHander(Object.keys(this.state.topics)[value])
    }

    onStateClickHandler (event)  {
        console.log(event)
    }

     getHexColor (value) {
        return utils.getColorGradient(value)
     }

     statesCustomConfig () { 
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

    fetchTopicHander (topic) {
        fetch(`http://localhost:8080/api/score/${topic}`).then((response) => {
            return response.json()
        }).catch((error) => {
            console.log(error)
        }).then((data) => { 
            this.setState({sentimentObj: data})
        })
    }

    componentWillMount () {
           fetch('http://localhost:8080/api/tags').then((response) => {
               return response.json()
           }).catch((error) => {
               console.log(error)
           }).then((data) => {
                this.setState({topics: data})
           })    

    }

    componentDidUpdate (prevprops, prevState) {

        if (this.state.topics != prevState.topics) {
          const topic = Object.keys(this.state.topics)[0]
          this.fetchTopicHander(topic)
        }
        
    }

    componentDidUpdate 
     render() {
        let divergingScheme = ["#93003a", "#ae1045", "#c52a52", "#d84360", "#e75d6f", "#f4777f", "#fd9291", "#ffaea5", "#ffcab9", "#ffe5cc", "#efec6b", "#deda5a", "#cac94b", "#b4b93e", "#9da932", "#849a26", "#6b8c1c", "#507e11", "#326f07", "#006100"]

        return (
            <div className="App">
                <div className="title">
                    Hello
                </div>
                
                <div className="popularTags">
                    {
                        Object.keys(this.state.topics).map((key, value) => {

                             return (<div class="button_cont" align="center" onClick={ () => this.onButtonClickHandlerpopularTags(value)}> 
                                          <a id={`topic_button_${value}`} class="topic_button" style={{background: this.state.senitmentID == value ? '#f6b93b': '' }} >
                                                {this.state.topics[key]}
                                          </a>
                                   </div>)
                        })
                    }

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
                            return <div  className='colormapItem' style={{backgroundColor: `${key}`}} id={`${key}-index`} ></div>
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

