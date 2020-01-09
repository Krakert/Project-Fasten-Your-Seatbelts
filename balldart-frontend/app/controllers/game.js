import Controller from '@ember/controller';
import { observer,computed } from '@ember/object'
import { set } from '@ember/object';
import { inject as service } from '@ember/service';
import { inject } from '@ember/controller';

export default Controller.extend({
  queryParams: ['gamemode','gamestate','username1','username2'],
  counter: 1,
  router: service(),
  application: inject('application'),

  seconds: computed('clock.second', function() {
    let x = this.get('clock.second');
    this.counter--;
    if(this.counter === 0){
      this.store.findRecord('game', 'board1').then((game)=>{
        if(game.round === 0 && this.gamestate === "1"){
          if(this.username1){
            this.store.findRecord('account', this.username1).then((account)=>{
              let pointsAccount = account.get('totalPoints');
              let pointsGame = game.get('pointsOne');
              console.log(pointsAccount, pointsGame);
              let addition = account.get('totalPoints') + game.get('pointsOne');
              console.log(addition);
              account.set('totalPoints', addition);


              account.save().then(()=>{
                game.set('mode',0);
                game.set('pointsOne',0);
                game.set('pointsTwo',0);
                game.save();
              });
              set(this,'gamestate', 2);
              this.application.set('incorrectNavbar', false);
            });
          }else{
            console.log("hoi")
            game.set('mode',0);
            game.set('pointsOne',0);
            game.set('pointsTwo',0);
            game.save();
            set(this,'gamestate', 2);
            this.application.set('incorrectNavbar', false);
          }
        }
        this.counter = 5;
      });
    }
    return x;
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
      console.log(state, mode);
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
      console.log(state, mode);
      set(this,'gamestate', state);
      this.model.save();
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
