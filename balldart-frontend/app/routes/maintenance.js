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
  }
});
