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
  enrichedModel: computed('model', function() {
    let array = [];
    let model = this.model;
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
