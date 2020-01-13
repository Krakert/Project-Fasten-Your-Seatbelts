import Controller from '@ember/controller';
import { observer } from '@ember/object'
import { set } from '@ember/object';
import { inject as service } from '@ember/service';
import { inject } from '@ember/controller';

export default Controller.extend({
  queryParams: ['gamemode','gamestate','username1','username2'],
  counter: 1,
  router: service(),
  application: inject('application'),

  seconds: observer('clock.second', function() {
    this.get('clock.second');
    this.counter--;
    if(this.counter === 0){
      this.store.findRecord('game', 'board1').then((game)=>{
        if(game.round === 0 && this.gamestate === "1"){
          if(this.username1 && game.mode === 1){
            this.store.findRecord('account', this.username1).then((account)=>{
              // Add to totalPoints
              let addition = account.get('totalPoints') + game.get('pointsOne');
              account.set('totalPoints', addition);

              // Highest Points Check
              if(game.get('pointsOne') > account.get('highestPoints')){
                account.set('highestPoints',game.get('pointsOne'));
              }
              // Number of rounds increased
              account.set('numberOfRounds', account.get('numberOfRounds') + 1);

              account.save().then(()=>{
                game.set('mode', 0);
                game.save();
              });
              set(this,'gamestate', 2);
              this.application.set('incorrectNavbar', false);
            });
          }else{
            game.set('mode', 0);
            game.save();
            set(this,'gamestate', 2);
            this.application.set('incorrectNavbar', false);
          }
        }
        this.counter = 5;
      });
    }
  }),

  actions: {
    nextGamestateSingleplayer: function(state,mode) {
      this.model.set('mode', mode)
      if(this.gamestate === "0"){
        this.application.set('incorrectNavbar', true);
        this.model.set('pointsOne', 0);
        this.model.set('round', 1);
        this.model.set('activePlayer', 1)
      }
      set(this,'gamestate', state);
      this.model.save();
    },
    nextGamestateMultiplayer: function(state,mode) {
      this.model.set('mode', mode)
      if(this.gamestate === "0"){
        this.application.set('incorrectNavbar', true);
        this.model.set('pointsOne', 0);
        this.model.set('pointsTwo', 0);
        this.model.set('round', 3);
        this.model.set('activePlayer', 1)
      }
      set(this,'gamestate', state);
      this.model.save();
    },
    replaySingle: function(){
      this.router.transitionTo('game', { queryParams: { gamemode: "singleplayer", gamestate: "0", username1: this.get('username1'), username2: ""}});
    },
    replayMultiple: function(){
      this.router.transitionTo('game', { queryParams: { gamemode: "multiplayer", gamestate: "0", username1: this.get('username1'), username2: this.get('username2')}});
    },
    homepage: function(){
      this.router.transitionTo('application');
    },
    stop: function(){
      this.application.set('incorrectNavbar', false);
      this.model.set('mode', 0);
      this.model.set('round', 0);
      this.router.transitionTo('application');
      this.model.save();
    }

  }
});
