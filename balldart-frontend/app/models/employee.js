import DS from 'ember-data';

export default DS.Model.extend({
  rfid: DS.attr(),
  active: DS.attr()
});
