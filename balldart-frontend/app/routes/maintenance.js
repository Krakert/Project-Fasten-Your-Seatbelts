import Route from '@ember/routing/route';
import { hash } from 'rsvp';

export default Route.extend({
  model: function() {
    var store = this.store;
    return hash({
      model: store.findAll('account'),
      employees: store.findAll('employee')
    });
  },
  setupController: function(controller, models) {
    controller.setProperties(models);
  },
  actions: {
    willTransition: function(){
      this.store.findRecord('employee',"fakeID").then((employee)=>{
        console.log(employee);
        employee.set('active', 0);
        employee.save();
      });
    }
  }
});
