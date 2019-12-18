import Controller from '@ember/controller';
//import { computed } from '@ember/object';

export default Controller.extend({
  queryParams: ['gamemode'],

  actions: {
    updateGame: function() {
      console.log('updateGame');
      this.model.save();
    }
  }
});
