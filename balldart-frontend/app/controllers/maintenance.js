import Controller from '@ember/controller';
import { observer  } from '@ember/object';
import { set } from '@ember/object';

export default Controller.extend({
  queryParams: [],
  counter: 1,
  active: 0,
  valid: false,

  seconds: observer('clock.second', function() {
    this.get('clock.second');
    this.counter--;
    if(this.counter === 0){
      this.store.findRecord('employee', '154162618071').then((employee)=>{
        set(this,'active', employee.active)
        this.counter = 1
      });
    }
  }),
  actions: {
    deleteAccount: function(account) {
      account.destroyRecord().then(()=>{
          this.store.unloadRecord(account);
      });
    },
    toggleLED: function(){
      this.store.findRecord('employee', '154162618071').then((employee)=>{
        employee.set('led', 1)
        employee.save();
      });
    },
    servoToOrigin: function(){
      this.store.findRecord('employee', '154162618071').then((employee)=>{
        employee.set('servo', 1)
        employee.save();
      });
    }
  }
});
