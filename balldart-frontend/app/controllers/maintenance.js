import Controller from '@ember/controller';
import { observer  } from '@ember/object';
import { set } from '@ember/object';
import { inject } from '@ember/controller';

export default Controller.extend({
  queryParams: [],
  counter: 1,
  active: 0,
  valid: false,
  seconds: observer('clock.second', function() {
    this.get('clock.second');
    this.counter--;
    if(this.counter === 0){
      this.store.findRecord('employee', 'fakeID').then((employee)=>{
        set(this,'active', employee.active)
        this.counter = 5
      });
    }
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
      } else{
        this.valid = true;
        employee.set('led', 0)
        employee.save();
      }
    }
  }
});
