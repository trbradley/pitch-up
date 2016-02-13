describe('NewEnrollmentController', function() {
  var ctrl;
  var scope;
  var windowMock;
  var EnrollmentsResourceMock;

  beforeEach(function() {
    windowMock = { location : { href: jasmine.createSpy() } };
    EnrollmentsResourceMock = jasmine.createSpyObj(
      'EnrollmentsResource', ['postEnrollments']
    );
    module('Pitchup', {
      EnrollmentsResource: EnrollmentsResourceMock,
      $window: windowMock
    });
  });

  beforeEach(inject(function($controller, $q, $rootScope) {
    EnrollmentsResourceMock.postEnrollments
      .and.returnValue($q.when({}));
    ctrl = $controller('NewEnrollmentController');
    scope = $rootScope;
  }));

  describe('#enroll', function() {
    it('redirects to /#/teams/:id', function() {
      ctrl.enroll();
      scope.$digest();
      expect(windowMock.location.href).toEqual('/#/teams/2');
    });
  });
});
