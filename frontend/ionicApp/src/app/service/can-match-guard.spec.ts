import { TestBed } from '@angular/core/testing';
import { CanMatchGuard } from './can-match-guard';
import { AuthService } from './auth';

describe('CanMatchGuard', () => {
  let guard: CanMatchGuard;
  let authService: jasmine.SpyObj<AuthService>;

  beforeEach(() => {
    authService = jasmine.createSpyObj('AuthService', ['getUserRoles']);

    TestBed.configureTestingModule({
      providers: [
        CanMatchGuard,
        { provide: AuthService, useValue: authService }
      ]
    });

    guard = TestBed.inject(CanMatchGuard);
  });

  it('allows access when user has allowed role', () => {
    authService.getRole.and.returnValue(0);

    const route: any = {
      data: { allowedRoles: [true,false,false,false,false] }
    };

    const result = guard.canMatch(route, []);

    expect(result).toBeTrue();
  });
});
