import Controller from '@ember/controller';
import { sort } from '@ember/object/computed'

export default Controller.extend({
  queryParams: ['data','sortingOrder'],
  todosSorting: Object.freeze(['totalPoints']),
  arrangedContent: sort('model', 'todosSorting'),
});
