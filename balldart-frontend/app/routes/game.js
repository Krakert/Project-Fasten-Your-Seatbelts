import Route from '@ember/routing/route';

export default Route.extend({
  model: function() {
    return this.store.findRecord('game', 'board1');
  },
  actions: {
    willTransition: function(){
      this.store.findRecord('game', 'board1').then((game)=>{
        game.set('pointsOne', 0);
        game.set('pointsTwo', 0);
        game.save();
      });
    }
  }
});
