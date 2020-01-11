import Controller from '@ember/controller';
import { sort } from '@ember/object/computed';
import { set, computed } from '@ember/object';

export default Controller.extend({
  queryParams: ['data'],
  arrangedContent: sort('enrichedModel', 'sortingOrder'),
  filtername: "",

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

  filteredModel: computed('model.@each.id','filtername', function() {
    let regex = new RegExp(this.filtername,'i');
    if(this.filtername !== ""){
      return this.model.filter((item)=>{
        return item.id.match(regex);
      });
    } else{
      return this.model;
    }
  }),
  enrichedModel: computed('filteredModel.@each.numberOfRounds', function() {
    let array = [];
    let model = this.filteredModel;
    if(model){
      model.forEach((m) => {
        let average = 0;
        if(m.numberOfRounds){
          average = Number(m.totalPoints) / Number(m.numberOfRounds);
        }
        m.set('averagePoints', average);
        array.push(m);
      })
    }
    return array;
  }),

  actions: {
    sort: function(data) {
      set(this,'data', data);

    }
  }
});
