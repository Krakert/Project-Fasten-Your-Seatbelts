import { module, test } from 'qunit';
import { setupTest } from 'ember-qunit';

module('Unit | Route | maintenance', function(hooks) {
  setupTest(hooks);

  test('it exists', function(assert) {
    let route = this.owner.lookup('route:maintenance');
    assert.ok(route);
  });
});
