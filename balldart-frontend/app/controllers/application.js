import Controller from '@ember/controller';
import { inject as service } from '@ember/service';
import { set } from '@ember/object';

export default Controller.extend({
    incorrectNavbar: false,
    router: service(),
    actions:{
      maintenance: function(){
        set('incorrectNavbar', false);
        this.router.transitionTo('application');
        this.model.save();
      }
    }
});
