import Controller from '@ember/controller';
import { set } from '@ember/object';

export default Controller.extend({
  queryParams: ['gamemode','gamestate','username'],

  actions: {
    nextGamestate: function(state,mode) {
      this.model.set('mode', mode)
      this.model.save();
      console.log(state, mode);
      set(this,'gamestate', state);
    }
  }
});
