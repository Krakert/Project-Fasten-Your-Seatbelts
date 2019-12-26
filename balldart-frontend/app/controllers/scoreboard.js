import Controller from '@ember/controller';
import { sort } from '@ember/object/computed'
import { set } from '@ember/object';

export default Controller.extend({
  queryParams: ['data'],
  todosSorting: Object.freeze(['data']),
  arrangedContent: sort('model', 'todosSorting'),

  actions: {
    sort: function(data) {
      set(this,'data', data);

    }
  }
});
