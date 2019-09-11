import React from 'react';
import { BrowserRouter as Router, Route} from "react-router-dom";
import {
  Grid,
  Button,
  Typography,
  Toolbar,
  AppBar,
  makeStyles
} from '@material-ui/core';

import VariableButtons from './components/variable_buttons.js'
import LeaderboardList from './components/leaderboards.js'
import './App.css';


const useStyles = makeStyles(theme => ({
  root: {
    flexGrow: 1,
  },
  title: {
    flexGrow: 1,
  },
  content: {
    marginTop: "2%",
    flex:1,
        flexDirection:'row',
        alignItems:'center',
        justifyContent:'center'
  },
  userInputs: {
    marginTop: "3%",
  },
}));


function RouteHome() {
  const classes = useStyles();

  return (
    <div>
      <div className={classes.userInputs}>
        <VariableButtons />
      </div>
    </div>
  );
}

function RouteLeaderBoards() {

  return (
    <Grid container direction="row" justify="space-evenly" alignItems="center" spacing={2}>
      <div>
          <LeaderboardList/>
      </div>
    </Grid>
  );
}

function App() {
  const classes = useStyles();
  
  return (
    <Router>
    <div className={classes.root}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" className={classes.title}>
            Mastermind
          </Typography>
          <Button color="inherit" onClick={() => {window.location.href = "/";}}>Home</Button>
          <Button color="inherit" onClick={() => {window.location.href = "/";}}>New Game</Button>
          <Button color="inherit" onClick={() => {window.location.href = "/leaderboards";}}>Leaderboards</Button>
        </Toolbar>
      </AppBar>
      <div className={classes.content}>
        <Route exact path="/" component={RouteHome} />
        <Route exact path="/leaderboards" component={RouteLeaderBoards} />
      </div>
    </div>
    </Router>
  );
}

export default App;
