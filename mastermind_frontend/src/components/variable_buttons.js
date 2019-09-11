import React from 'react';
import {
  Chip,
  Fab,
  Grid,
  Button
} from '@material-ui/core';


  class VariableButtons extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
          selections: [],
          submits: [],
          username: 'Bruce_the_bat_32',
          game_id: ''
       };
     }
    
    createGame(){
      var currentUsername = this.state.username;
      fetch(`http://127.0.0.1:8000/api/game/create_game?username=${currentUsername}`)
      .then(response => response.json())
      .then(resData => {
        console.log("Current GameID: ", resData.game_id)
        this.setState({ game_id: resData.game_id});
      });
    }
    
    checkResults(){
      var currentGameID = this.state.game_id;
      var currentUsername = this.state.username;
      var submitSelection = this.state.selections.join(",");
      fetch(`http://127.0.0.1:8000/api/game/make_move?username=${currentUsername}&game_id=${currentGameID}&variables=${submitSelection}`)
      .then(response => response.json())
      .then(resData => {
        if (resData.status === "sequence.error"){
          alert(resData.message + " However, [ " + resData.correct_variables + " ] was correct.")
        } else if(resData.status === "sequence.too_many_variables"){
          alert(resData.message)
        } else if(resData.status === "sequence.error.max_retrys"){
          alert(resData.message + ", Please start a new game")
        } else if(resData.status === "sequence.solved"){
          alert(resData.message + ", Please start a new game")
        }

      });
    }

    addInput(event, value){
      var newSelections = this.state.selections;
      var index = newSelections.indexOf(value);
      if(index > -1){
        newSelections.splice(index, 1);
      } else {
        newSelections.push(value);
      }
      this.setState({ selections: newSelections });
    }

    submitInputs(event){
      var currentSelections = this.state.selections;
      var currentSubmits = this.state.submits;
      currentSubmits.push(currentSelections)
      this.setState({ submits: currentSubmits });
      
      this.checkResults()
      // Clear and Cleanup
      this.setState({ selections: [] });
    }
    
    handleChange(event) {
      this.setState({ username: event.target.value });
    }

    async componentDidMount() {
      this.createGame();
    }
    
    render() {
      const style = {
        margin: '0.5em',
        paddingLeft: 0,
        listStyle: 'none'
      };

      return (
        (<Grid container spacing={2}>
          
          <Grid item xs={12}>
            <Grid container justify="center" spacing={1}>
            {this.state.selections.map((value, index) => (
                <div key={index}>
                  <Chip
                  variant="outlined"
                  size="small"
                  label={value}
                />
                </div>
                  ))}
            </Grid>
          </Grid>
          <Grid item xs={12}>
              <Grid container justify="center" spacing={1}>
                  {[0, 1, 2, 3, 4, 5, 6, 7, 8, 9].map(value => (
                  <Grid key={value} item>
                      <Fab color="inherit" aria-label="add" onClick={(event) => { this.addInput(event, value); }}>
                      {value}
                      </Fab>
                  </Grid>
                  ))}
                  <Button variant="contained" color="primary" onClick={(event) => { this.submitInputs(event); }}>Submit</Button>
              </Grid>
          </Grid>
          <Grid item xs={12}>
          {this.state.submits.map((guess, guess_id) => (
              <Grid container justify="center" key={guess_id} spacing={1}>Guess #{guess_id}
                  {guess.map((value, index) => (
                    <div key={index} style={style}>
                      <Chip
                      variant="outlined"
                      size="small"
                      label={value}
                    />
                    </div>
                  ))}
              </Grid>
              ))}
          </Grid>
      </Grid>)
        );
      }
  }


export default VariableButtons;
