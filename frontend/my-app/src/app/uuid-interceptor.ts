import { Injectable } from '@angular/core';
import {
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest
} from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth';

@Injectable()
export class UuidInterceptor implements HttpInterceptor {

  constructor(private authService: AuthService) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const uuid = this.authService.getUuid();
    if (!uuid) return next.handle(req);

    const cloned = req.clone({
      setHeaders: { 'X-Client-UUID': uuid }
    });

    return next.handle(cloned);
  }
}
