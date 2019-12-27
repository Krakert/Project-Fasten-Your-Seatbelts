import Controller from '@ember/controller';
import { computed } from '@ember/object'
export default Controller.extend({
  queryParams: ['active'],
  counter: 1,
  valid: false,
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
    },
    toggleLED: function(){
      let employee = this.employees.get('firstObject');
      if(this.valid){
        this.valid = false
        employee.set('led', 1)
        employee.save();
      }else{
        this.valid = true;
        employee.set('led', 0)
        employee.save();
      }
    }
  }
});
