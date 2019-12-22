import Controller from '@ember/controller';

export default Controller.extend({

  actions: {
    deleteAccount: function(account) {
      account.destroyRecord();
    }
  }
});
