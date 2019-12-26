import Controller from '@ember/controller';
import { computed } from '@ember/object'
export default Controller.extend({
  queryParams: ['active'],
  counter: 1,
  seconds: computed('clock.second', function() {
    let x = this.get('clock.second');
    this.counter--;
    if(this.counter === 0){
      this.store.findRecord('employee', 'fakeID');
      this.active = this.model.active;
      console.log('x', x);
      this.counter = 5
    }
    return x;
  }),
  actions: {
    deleteAccount: function(account) {
      account.destroyRecord();
    }
  }
});
