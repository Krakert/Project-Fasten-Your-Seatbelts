import DS from 'ember-data';

export default DS.Model.extend({
    // username
    password: DS.attr(),
    totalPoints: DS.attr(),
    highestPoints: DS.attr(),
    numberOfRounds: DS.attr(),
    latestRound: DS.attr()
});
