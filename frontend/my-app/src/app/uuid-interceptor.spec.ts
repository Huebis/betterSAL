import { TestBed } from '@angular/core/testing';
import { HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http';
import { of } from 'rxjs';
import { UuidInterceptor } from './uuid-interceptor';
import { AuthService } from './auth';

describe('UuidInterceptor', () => {
  let interceptor: UuidInterceptor;
  let authService: AuthService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        AuthService,
        UuidInterceptor
      ]
    });

    interceptor = TestBed.inject(UuidInterceptor);
    authService = TestBed.inject(AuthService);
  });

  it('should add X-Client-UUID header if UUID exists', (done) => {
    // Arrange: set a UUID
    authService.setUuid('1234-5678-uuid-example');

    const req = new HttpRequest('GET', '/test');
    
    const next: HttpHandler = {
      handle: (request: HttpRequest<any>) => {
        // Assert
        expect(request.headers.has('X-Client-UUID')).toBe(true);
        expect(request.headers.get('X-Client-UUID')).toBe('1234-5678-uuid-example');
        return of({} as HttpEvent<any>);
      }
    };

    // Act
    interceptor.intercept(req, next).subscribe(() => {
      done();
    });
  });

  it('should not add header if UUID is missing', (done) => {
    authService.clearUuid();

    const req = new HttpRequest('GET', '/test');

    const next: HttpHandler = {
      handle: (request: HttpRequest<any>) => {
        expect(request.headers.has('X-Client-UUID')).toBe(false);
        return of({} as HttpEvent<any>);
      }
    };

    interceptor.intercept(req, next).subscribe(() => {
      done();
    });
  });
});
