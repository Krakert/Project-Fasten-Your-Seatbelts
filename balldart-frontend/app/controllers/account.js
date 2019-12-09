import Controller from '@ember/controller';
import { inject as service } from '@ember/service'

export default Controller.extend({
  queryParams: ['accountmode'],
  router: service(),

  actions: {
    createAccount(){
      console.log("we komen er");
      console.log(this.get('username'));
      console.log(this.get('password1'));
      let newAccount = this.store.createRecord('account',{
        id: this.get('username'),
        password: this.get('password1')
      });
      this.router.transitionTo('game',{ queryParams: { gamemode: "singleplayer"}}, newAccount.save());
    },
    login(){

    }
  }
});
