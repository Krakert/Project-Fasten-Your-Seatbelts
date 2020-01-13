import Controller from '@ember/controller';
import { observer, computed,  } from '@ember/object';
import { set } from '@ember/object';
import { filterBy } from '@ember/object/computed';

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
        set(this,'active', employee.active);
        this.counter = 1;
      });
    }
  }),

  employee: filterBy('employees','id', '154162618071'),

  systemRuntime: computed('employee.@each.runtimeSystemInSec', function(){
    if(this.employee[0].runtimeSystemInSec >= 3600){
      return Math.floor(this.employee[0].runtimeSystemInSec) + " secondes, checken dus!";
    } else{
      return Math.floor(this.employee[0].runtimeSystemInSec) + " seconde(s), prima!";
    }
  }),
  servoRuntime: computed('employee.@each.runtimeServoInSec', function(){
    if(this.employee[0].runtimeServoInSec >= 3600){
      return Math.floor(this.employee[0].runtimeServoInSec) + " secondes, checken dus!";
    } else{
      return Math.floor(this.employee[0].runtimeServoInSec) + " seconde(s), prima!";
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
        employee.set('led', 1);
        employee.save();
      });
    },
    servoToOrigin: function(){
      this.store.findRecord('employee', '154162618071').then((employee)=>{
        employee.set('servo', 1);
        employee.save();
      });
    },
    clearSystemRuntime: function(){
      this.store.findRecord('employee', '154162618071').then((employee)=>{
        employee.set('runtimeSystemInSec', 0);
        employee.save();
      });
    },
    clearServoRuntime: function(){
      this.store.findRecord('employee', '154162618071').then((employee)=>{
        employee.set('runtimeServoInSec', 0);
        employee.save();
      });
    },
  }
});
