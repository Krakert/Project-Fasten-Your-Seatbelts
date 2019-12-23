import Controller from '@ember/controller';
import { set } from '@ember/object';

export default Controller.extend({
  queryParams: ['gamemode','gamestate','username1','username2'],

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
    increasePoints: function(player){
      if(player === 1){
        this.model.set('pointsOne', this.model.pointsOne + 1);
      }
      if (player === 2){
        this.model.set('pointsTwo', this.model.pointsTwo + 1);
      }
      this.model.save();
    }
  }
});
