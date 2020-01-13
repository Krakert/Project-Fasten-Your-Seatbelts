import DS from 'ember-data';

export default DS.Model.extend({
  active: DS.attr(),
  led: DS.attr(),
  servo: DS.attr(),
  runtimeSystemInSec: DS.attr(),
  runtimeServoInSec: DS.attr()
});
