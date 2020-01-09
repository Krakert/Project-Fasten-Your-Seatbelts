import Controller from '@ember/controller';
import { inject as service } from '@ember/service';
import { set } from '@ember/object';

export default Controller.extend({
  queryParams: ['accountmode'],
  router: service(),
  errorMessage: false,

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
        this.router.transitionTo('game', { queryParams: { gamemode: "singleplayer", gamestate: "0", username1: this.get('username'), username2: ""}});
        set(this,'username',"");
        set(this,'password1',"");
        set(this,'password2',"");
      })
    },
    login(){
      this.store.findRecord('account', this.get('username'))
        .then((account)=>{
          if(account.password === this.get('password1')){
            set(this, 'errorMessage', false);
            this.router.transitionTo('game', { queryParams: { gamemode: "singleplayer", gamestate: "0", username1: this.get('username'), username2: ""}});
            set(this,'username',"");
            set(this,'password1',"");
            set(this,'password2',"");
          } else {
            set(this, 'errorMessage', true);
          }
        }).catch(()=>{
          set(this, 'errorMessage', true);
      });
    }
  }
});
