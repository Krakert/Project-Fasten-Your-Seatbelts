import Controller from '@ember/controller';
import { inject as service } from '@ember/service'

export default Controller.extend({
  queryParams: ['accountmode'],
  router: service(),

  actions: {
    createAccount(){
      let newAccount = this.store.createRecord('account',{
        id: this.get('username'),
        password: this.get('password1'),
        totalPoints: 0,
        highestPoints: 0,
        numberOfRounds: 0,
        latestRound: 0,

      });
      newAccount.save().then(()=>{
        this.router.transitionTo('game', { queryParams: { gamemode: "singleplayer"}});
      })
      this.username = "";
      this.password1 = "";
      this.password2 = "";
    },
    login(){
      this.username = "";
      this.password1 = "";
      this.password2 = "";
    }
  }
});
