import Controller from '@ember/controller';

export default Controller.extend({
  actions: {
    back: function() {
        window.history.back();
    }
  }
});
