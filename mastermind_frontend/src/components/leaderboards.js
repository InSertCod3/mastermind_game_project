import React from 'react';
import {
  ListItem,
  ListItemText,
  List,
} from '@material-ui/core';



class LeaderboardList extends React.Component {
  constructor(props) {
      super(props);
      this.state = {
        data: [{"username": null, "completed_games": null}],
     };
   }
  
  grabLeaderboards(){
    fetch("http://127.0.0.1:8000/api/game/leaderboards")
    .then(response => response.json())
    .then(resData => {
      var data = [];
      for (var x in resData.board){
        data.push({"username": x, "completed_games": resData.board[x].completed_games});
      }
      this.setState({ data: data });
    });
  }
  
  static async getDerivedStateFromProps(props, state) {

  }

  async componentDidMount() {
    this.grabLeaderboards();
  }
  
  render() {
    return (
        <div>
          <List>
              {this.state.data.map((item, index) => (
                  <ListItem key={index} button>
                    <ListItemText primary={item.username + " ~ Games Completed : " + item.completed_games} />
                  </ListItem>
              ))}
          </List>
      </div>
      );
    }
}


export default LeaderboardList;
