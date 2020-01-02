import Controller from '@ember/controller';
import { observer } from '@ember/object'
import { set } from '@ember/object';
import { inject as service } from '@ember/service';
export default Controller.extend({
  queryParams: ['gamemode','gamestate','username1','username2'],
  counter: 1,
  router: service(),

  seconds: observer('clock.second', function() {
    let x = this.get('clock.second');
    this.counter--;
    if(this.counter === 0){
      this.store.findRecord('game', 'board1');
      console.log('x', x);
      this.counter = 5
    }
  }),

  actions: {
    nextGamestateSingleplayer: function(state,mode) {
      this.model.set('mode', mode)
      if(this.gamestate === "0"){
        this.model.set('pointsOne', 0);
        this.model.set('round', 3);
        this.model.set('activePlayer', 1)
      }
      console.log(state, mode);
      set(this,'gamestate', state);
      this.model.save();
    },
    nextGamestateMultiplayer: function(state,mode) {
      this.model.set('mode', mode)
      if(this.gamestate === "0"){
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
      this.model.set('mode', 0);
      this.model.set('round', 0);
      this.router.transitionTo('application');
      this.model.save();
    }

  }
});
