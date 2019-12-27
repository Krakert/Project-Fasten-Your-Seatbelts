import Controller from '@ember/controller';
import { sort } from '@ember/object/computed';
import { set, computed } from '@ember/object';

export default Controller.extend({
  queryParams: ['data'],
  arrangedContent: sort('enrichedModel', 'sortingOrder'),

  sortingOrder: computed('data', function() {
    let data = this.data;
    if(data === "totalPoints"){
      return ["totalPoints:desc"];
    } else if(data === "highestPoints"){
      return ["highestPoints:desc"];
    } else{
      return ["averagePoints:desc"];
    }
  }),

  // filteredModel: filter('model',function(item){
  //   return item.id === this.filtername;
  // }),
  // filteredModel: computed('model.@each.id', 'filtername', function(){
  //   return this.model.filter(function(item){ return item.id === this.filtername});
  // }),

   filteredModel: computed('model.@each.id','filtername', function(item) {
     if(item.id === this.filtername){
       return this.model.filterBy('id', this.filtername);
     }
     return this.model;
   }),
  enrichedModel: computed('filteredModel', function() {
    let array = [];
    let model = this.filteredModel;
    console.log(model);
    if(model){
      model.forEach((m) => {
        let average = 0;
        if(m.numberOfRounds){
          average = Number(m.totalPoints) / Number(m.numberOfRounds);
        }
        m.set('averagePoints', average);
        array.push(m);
      })
      console.log(array);
    }
    return array;
  }),

  actions: {
    sort: function(data) {
      set(this,'data', data);

    }
  }
});
