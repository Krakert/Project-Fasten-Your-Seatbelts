import DS from 'ember-data';

export default DS.Model.extend({
  mode: DS.attr(),
  round: DS.attr(),
  pointsOne: DS.attr(),
  pointsTwo: DS.attr(),
  activePlayer: DS.attr()
});
